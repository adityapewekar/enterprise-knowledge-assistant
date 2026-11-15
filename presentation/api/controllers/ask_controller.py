import json
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, UploadFile
from application.services.converstation_service import (
    get_context_messages,
    save_exchange,
)
from infrastructure.authentication import get_current_user
from infrastructure.langgraph_service import run_agent
from infrastructure.file_service import parse_doc
from presentation.api.request_dtos.ask_request_dto import AskRequestDto

ask_router = APIRouter()


@ask_router.post("/ask")
def ask(
    request: AskRequestDto,
    current_user_id: str = Depends(get_current_user),
    role: Annotated[str | None, Header(alias="x-role")] = None,
):
    print(f"Received query: {request.query}")

    effective_role = request.role or role or "guest"
    print(f"Effective role: {effective_role}")

    try:
        history = get_context_messages(current_user_id)
        result = run_agent(request.query, effective_role, history)
        if not isinstance(result, dict):
            result = {"response": str(result)}

        if "error" not in result:
            answer = result.get("response") or result.get("message")
            if not isinstance(answer, str):
                answer = str(answer) if answer is not None else json.dumps(result, ensure_ascii=False)
            result["response"] = answer
            save_exchange(current_user_id, request.query, answer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to process or save this conversation.") from exc

    print(f"Agent response: {result}")
    return result


@ask_router.post("/upload_doc")
async def upload_doc(file: UploadFile):
    text = parse_doc(file)
    return {"parsed_text": text[:500]}
