from domain.ports import ConversationRepository


class ConversationService:
    def __init__(self, repository: ConversationRepository):
        self._repository = repository

    def get_conversation_messages(self, user_id: str) -> list[dict[str, str]]:
        return self._repository.get_conversation(user_id)

    def get_context_messages(self, user_id: str) -> list[dict[str, str]]:
        return self._repository.get_context(user_id)

    def save_exchange(self, user_id: str, user_message: str, assistant_message: str) -> None:
        self._repository.save_exchange(user_id, user_message, assistant_message)

    def clear_conversation(self, user_id: str) -> None:
        self._repository.clear_conversation(user_id)
