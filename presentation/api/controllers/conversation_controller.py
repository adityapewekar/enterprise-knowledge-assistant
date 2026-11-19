
from fastapi import APIRouter, Depends, HTTPException

from application.services.conversation_service import ConversationService
from presentation.api.dependencies.authentication import get_current_user
from presentation.api.dependencies.services import get_conversation_service


conversation_router = APIRouter()

@conversation_router.get("/conversations/me/messages")
def read(
    current_user_id: str = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    try:
        messages = service.get_conversation_messages(current_user_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to load conversation history.") from exc
    return {"messages": messages}


@conversation_router.delete("/conversations/me/messages")
def delete(
    current_user_id: str = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    try:
        service.clear_conversation(current_user_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to clear conversation history.") from exc
    return {"cleared": True}

