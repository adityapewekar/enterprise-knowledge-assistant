import os
import uuid

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from infrastructure.mcp_service import mcp_tools

load_dotenv()

def fallback_tool(query):
    return {
        "found": False,
        "message": "⚠️ No tool available for this query. The agent is restricted to KBSearch and DBFetch."
    }

tools = [
    Tool(
        name="KBSearch",
        func=mcp_tools["KBSearch"].run,
        description=(
            "Use this tool to search the internal company knowledge base for policies, guidelines, and conduct documents. "
            "It first attempts an exact or semantic match using embeddings. If no exact match is found, it will provide "
            "query-driven suggestions based on partial or lexical matches. Always return results in the format "
            "{found, query, results, suggestions, message}. If 'found' is true, use the 'results' directly. "
            "If 'found' is false but 'suggestions' are present, present them as possible alternatives."
        )
    ),
    Tool(
        name="DBFetch",
        func=mcp_tools["DBFetch"].run,
        description=(
        "Use this tool to look up information from the correct table in the SQLite database. "
        "For employee queries, use the 'employees' table. "
        "For project lead queries, use the 'projects' table. "
        "For department manager queries, use the 'departments' table. "
        "It returns {found, source_table, name, email, message}."
        )
    ),
    Tool(
        name="Fallback",
        func=fallback_tool,
        description=(
            "Use this tool when the query does not match KBSearch or DBFetch. "
            "It handles unsupported queries, external world knowledge, or public figures. "
            "It always returns {found: false, message}."
        ),
    )
]

agent = None
if os.getenv("OPENAI_API_KEY"):
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    agent = create_agent(model=llm, tools=tools)


def run_agent(query):
    print(f"Running agent for query: {query}")
    if agent is None:
        return {"error": "OpenAI API key is not configured."}

    try:
        response = agent.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"configurable": {"session_id": str(uuid.uuid4())}}
        )
        print(f"Agent response: {response}")

        # Ensure response is a dict
        messages = response.get("messages", []) if isinstance(response, dict) else []
        if messages:
            latest_answer = None
            for message in reversed(messages):
                content = getattr(message, "content", None)

                # Handle structured tool outputs (dicts with suggestions)
                if isinstance(content, dict):
                    # If tool returned suggestions
                    if "suggestions" in content and content["suggestions"]:
                        return {
                            "response": content.get("message", "No exact match found."),
                            "suggestions": content["suggestions"],
                            "found": content.get("found", False),
                            "query": content.get("query", query)
                        }
                    # Normal tool response
                    return content

                # Handle string content
                if isinstance(content, list):
                    content = "\n".join(str(item) for item in content)
                if isinstance(content, str) and content.strip():
                    if getattr(message, "type", None) == "ai" or getattr(message, "role", None) == "assistant":
                        latest_answer = content
                        break

            if latest_answer is not None:
                return {"response": latest_answer}

            # Fallback to last message content
            last_message = messages[-1]
            content = getattr(last_message, "content", None)
            if isinstance(content, list):
                content = "\n".join(str(item) for item in content)
            print(f"Last message content: {content}")
            print(f"response object: {response}")
            return {"response": content or str(last_message)}

        print(f"response object: {response}")
        return {"response": str(response)}

    except Exception as exc:
        print(exc)
        return {"error": f"Agent execution failed: {exc}"}

