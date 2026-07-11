from pydantic import BaseModel


class KBRequestDto(BaseModel):
    article: str
    roles: list[str]