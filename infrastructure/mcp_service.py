from langgraph.prebuilt import ToolRuntime

from infrastructure.sqlite_db_service import db_router
from infrastructure.chroma_db_service import search_kb

class MCPContext:
    def __init__(self, name, funv):
        self.name = name
        self.funv = funv

    def run(self, tool_input, runtime: ToolRuntime, **kwargs):
        print(f"[Middleware] MCPContext.run called with tool_input={tool_input}, runtime={runtime}")

        payload = {}
        if isinstance(tool_input, dict):
            payload.update(tool_input)
        else:
            payload["query"] = tool_input

        # Access role from context_schema
        role = None
        if runtime is not None and hasattr(runtime, "context"):
            role = getattr(runtime.context, "role", None)

        payload["role"] = role or "guest"
        print("--------------------------------")
        print(f"[Middleware] MCPContext.run payload: {payload}")
        print("--------------------------------")

        return self.funv(**payload)

mcp_tools = {
    "KBSearch": MCPContext("KBSearch", search_kb),
    "DBFetch": MCPContext("DBFetch", db_router),
}
