from pydantic import BaseModel


class AskRequest(BaseModel):
    query: str
    role: str | None = None