from typing import Protocol


class AgentPort(Protocol):
    def run(self, query: str, role: str, history: list[dict[str, str]]) -> dict:
        ...


class ConversationRepository(Protocol):
    def get_conversation(self, user_id: str) -> list[dict[str, str]]:
        ...

    def get_context(self, user_id: str) -> list[dict[str, str]]:
        ...

    def save_exchange(self, user_id: str, user_message: str, assistant_message: str) -> None:
        ...

    def clear_conversation(self, user_id: str) -> None:
        ...


class KnowledgeBase(Protocol):
    def update_article(self, article: str, roles: list[str]) -> dict:
        ...


class DocumentParser(Protocol):
    def parse(self, filename: str, content: bytes) -> str:
        ...
