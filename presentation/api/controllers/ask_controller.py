from typing import Annotated

from fastapi import APIRouter, Depends,  Header, HTTPException
from presentation.api.dependencies.authentication import get_current_user
from presentation.api.dependencies.services import get_ask_service
from application.services.ask_service import AskService
from presentation.api.request_dtos.ask_request_dto import AskRequestDto

ask_router = APIRouter()


@ask_router.post("/ask")
def ask(
    request: AskRequestDto,
    current_user_id: str = Depends(get_current_user),
    role: Annotated[str | None, Header(alias="x-role")] = None,
    service: AskService = Depends(get_ask_service),
):
    print(f"Received query: {request.query}")

    effective_role = request.role or role or "guest"
    print(f"Effective role: {effective_role}")

    try:
        result = service.ask(current_user_id, request.query, effective_role)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to process or save this conversation.") from exc

    print(f"Agent response: {result}")
    return result
