from infrastructure.sqlite_db_service import fetch_users
from infrastructure.chroma_db_service import search_kb


class MCPContext:
    def __init__(self, name,funv):
        self.name = name
        self.funv = funv

    def run(self,query): return self.funv(query)

mcp_tools = {
    "KBSearch":MCPContext("KBSearch", search_kb),
    "DBFetch":MCPContext("DBFetch", fetch_users)
}

