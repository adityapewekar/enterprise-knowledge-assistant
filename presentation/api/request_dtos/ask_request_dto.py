from pydantic import BaseModel


class AskRequestDto(BaseModel):
    query: str
    role: str | None = None