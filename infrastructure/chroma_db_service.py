from difflib import SequenceMatcher
import os
import re

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

from fuzzywuzzy import fuzz

load_dotenv()

document_objects = [
    Document(
        page_content="Company Password Policy: All employees must change their passwords every 90 days and use a combination of letters, numbers, and special characters.",
        metadata={"roles": ["admin", "employee"]}
    ),
    Document(
        page_content="Employee Handbook: Our company values integrity, teamwork, and innovation. We encourage open communication and continuous learning.",
        metadata={"roles": ["admin", "employee"]}
    ),
    Document(
        page_content="IT Security Guidelines: Employees should not share their login credentials and must report any suspicious activity to the IT department immediately.",
        metadata={"roles": ["admin", "employee"]}
    ),
    Document(
        page_content="Remote Work Policy: Employees are allowed to work remotely up to two days a week, provided they have prior approval from their manager.",
        metadata={"roles": ["admin", "employee"]}
    ),
    Document(
        page_content="Code of Conduct: All employees are expected to treat each other with respect and professionalism, and any form of harassment or discrimination will not be tolerated.", 
        metadata={"roles": ["admin", "employee"]}
    ),
    Document(
        page_content="Confidential Audit Policy: This document details the internal audit procedures, including financial compliance checks and risk assessments, and is restricted to administrators due to its sensitive nature.",
        metadata={"roles": ["admin"]}
    ),
    Document(
        page_content="Strategic Roadmap 2026: This document outlines the companys long term vision, investment priorities, and expansion plans for the next fiscal years, and is accessible only to administrators to protect strategic confidentiality.",
        metadata={"roles": ["admin"]}
    )
]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
embedding_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

db = Chroma(
    embedding_function=embedding_model,
    collection_name="eka_kb_docs",
    persist_directory="./chroma_db"
)

collection = db._collection

print(f"Chroma DB initialized. Document count: {collection.count()}")

if embedding_model and collection.count() == 0:
    db = Chroma.from_documents(
        documents=document_objects,
        embedding=embedding_model,
        collection_name="eka_kb_docs",
        persist_directory="./chroma_db"
    )


def _score_document(query, text):
    return fuzz.partial_ratio(query.lower(), text.lower())


def search_kb(query,role="guest"):
    print(f"Searching knowledge base for query: {query}")
    if not client or not db:
        return {"found": False, "query": query, "results": None, "message": "Knowledge base is unavailable because OpenAI credentials are not configured."}

    query_embedding = embedding_model.embed_query(query)
    similarity_results = db.similarity_search_by_vector(query_embedding, k=5)
    print(f"Similarity search results: {similarity_results}")
    similarity_results = [doc for doc in similarity_results if role in doc.metadata.get("roles", [])]
    similarity_content = [result.page_content for result in similarity_results if getattr(result, "page_content", None)]

    if similarity_content:
        similarity_scored = [(_score_document(query, text), text) for text in similarity_content]
        similarity_scored.sort(key=lambda item: item[0], reverse=True)
        print(f"Scored similarity results: {similarity_scored}")
        exact_matches = [text for score, text in similarity_scored if score > 70]
        # If top score is strong (exact match), return it
        print(f"Exact matches found: {exact_matches}")
        if exact_matches:
            if len(exact_matches) == 1:            
                return {
                    "found": True,
                    "query": query,
                    "results": similarity_scored[0][1],
                    "suggestions": [],
                    "message": "Exact match found."
                }
            else:
            # Multiple exact matches → return as suggestions
                return {
                    "found": False,
                    "query": query,
                    "results": None,
                    "suggestions": exact_matches,
                    "message": "Multiple exact matches found. Suggestions provided."
                }

   # Otherwise, treat as broad query → return suggestions
    suggestions = [text for score, text in similarity_scored if score > 0]
    print(f"Suggestions based on query: {suggestions}")
    if suggestions:
        return {
            "found": False,
            "query": query,
            "results": None,
            "suggestions": suggestions,
            "message": "No exact match found. Suggestions based on query provided." if suggestions else "No relevant KB result."
        }

def update_kb_article(request):
    if not client or not db:
        return {"success": False, "message": "Knowledge base is unavailable because OpenAI credentials are not configured."}

    new_doc = Document(
        page_content=request.article,
        metadata={"roles": request.roles}
    )
    db.add_documents([new_doc])
    return {"success": True, "message": "Knowledge base updated successfully."}