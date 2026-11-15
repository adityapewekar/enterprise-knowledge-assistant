from infrastructure.db.sqlite.conversation_db_service import (
    clear_conversation_by_user,
    get_context_by_user,
    get_conversation_by_user,
    save_conversation_exchange,
)


def get_conversation_messages(user_id: str) -> list[dict[str, str]]:
    return get_conversation_by_user(user_id)

def get_context_messages(user_id: str) -> list[dict[str, str]]:
    return get_context_by_user(user_id)

def save_exchange(user_id: str, user_message: str, assistant_message: str):
    return save_conversation_exchange(user_id, user_message, assistant_message)

def clear_conversation(user_id: str):
    return clear_conversation_by_user(user_id)
