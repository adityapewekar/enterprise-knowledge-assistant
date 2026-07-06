import os
import re

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv()

docs = [
    "Company Password Policy: All employees must change their passwords every 90 days and use a combination of letters, numbers, and special characters.",
    "Employee Handbook: Our company values integrity, teamwork, and innovation. We encourage open communication and continuous learning.",
    "IT Security Guidelines: Employees should not share their login credentials and must report any suspicious activity to the IT department immediately.",
    "Remote Work Policy: Employees are allowed to work remotely up to two days a week, provided they have prior approval from their manager.",
    "Code of Conduct: All employees are expected to treat each other with respect and professionalism, and any form of harassment or discrimination will not be tolerated."
]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
embedding_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

db = Chroma(
    embedding_function=embedding_model,
    collection_name="eka_kb_docs",
    persist_directory="./chroma_db"
)
db.delete_collection()

if embedding_model:
    document_objects = [Document(page_content=text) for text in docs]
    db = Chroma.from_documents(
        documents=document_objects,
        embedding=embedding_model,
        collection_name="eka_kb_docs",
        persist_directory="./chroma_db"
    )
else:
    db = None


def _score_document(query, text):
    normalized_query = query.lower()
    lowered_text = text.lower()

    if normalized_query in lowered_text:
        return 100

    query_terms = set(re.findall(r"[a-z0-9]+", normalized_query))
    text_terms = set(re.findall(r"[a-z0-9]+", lowered_text))
    overlap = len(query_terms.intersection(text_terms))
    return overlap


def search_kb(query):
    print(f"Searching knowledge base for query: {query}")
    if not client or not db:
        return {"found": False, "query": query, "results": None, "message": "Knowledge base is unavailable because OpenAI credentials are not configured."}

    query_embedding = embedding_model.embed_query(query)
    similarity_results = db.similarity_search_by_vector(query_embedding, k=3)
    print(f"Similarity search results: {similarity_results}")
    similarity_content = [result.page_content for result in similarity_results if getattr(result, "page_content", None)]

    if similarity_content:
        similarity_scored = [(_score_document(query, text), text) for text in similarity_content]
        similarity_scored.sort(key=lambda item: item[0], reverse=True)
        best_result = similarity_scored[0][1] if similarity_scored else None
        print(f"Best similarity result: {best_result}")
        if best_result:
            return {
                "found": True,
                "query": query,
                "results": best_result,
                "message": "Knowledge base lookup completed.",
            }

    lexical_results = []
    for document_text in docs:
        lexical_results.append((_score_document(query, document_text), document_text))
    lexical_results.sort(key=lambda item: item[0], reverse=True)
    fallback_result = lexical_results[0][1] if lexical_results else None
    print(f"Fallback result: {fallback_result}")

    return {
        "found": bool(fallback_result),
        "query": query,
        "results": fallback_result,
        "message": "Knowledge base lookup completed." if fallback_result else "No relevant knowledge base result was found.",
    }