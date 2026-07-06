import os
import uuid

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from Infrastructure.mcp_service import mcp_tools

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
            "Use this tool ONLY to search the internal company knowledge base. "
            "It is restricted to company policies, HR guidelines, and internal documents. "
            "Do NOT use it for general world knowledge, public figures, or external facts. "
            "It returns {found, query, results, message}."
        )
    ),
    Tool(
        name="DBFetch",
        func=mcp_tools["DBFetch"].run,
        description=(
            "Use this tool ONLY to look up employee information in the company database. "
            "It is restricted to internal employee records such as names and email addresses. "
            "Do NOT use it for external people or public figures. "
            "It returns {found, name, email}."
        ),
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
        response = agent.invoke({"messages": [HumanMessage(content=query)]},
                                    config={"configurable": {"session_id": str(uuid.uuid4())}})
        print(f"Agent response: {response}")
        messages = response.get("messages", []) if isinstance(response, dict) else []
        if messages:
            latest_answer = None
            for message in reversed(messages):
                content = getattr(message, "content", None)
                if isinstance(content, list):
                    content = "\n".join(str(item) for item in content)
                if isinstance(content, str) and content.strip():
                    if getattr(message, "type", None) == "ai" or getattr(message, "role", None) == "assistant":
                        latest_answer = content
                        break
            if latest_answer is not None:
                return {"response": latest_answer}

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
