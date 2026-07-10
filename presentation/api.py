from typing import Annotated

from fastapi import APIRouter, Header, UploadFile
from infrastructure.langgraph_service import run_agent
from infrastructure.file_service import parse_doc
from domain.models.ask_request import AskRequest

router = APIRouter()


@router.post("/ask")
def ask(request: AskRequest, role: Annotated[str | None, Header(alias="x-role")] = None):
    print(f"Received query: {request.query}")

    effective_role = request.role or role or "guest"
    print(f"Effective role: {effective_role}")

    result = run_agent(request.query, effective_role)
    print(f"Agent response: {result}")
    return result


@router.post("/upload_doc")
async def upload_doc(file: UploadFile):
    text = parse_doc(file)
    return {"parsed_text": text[:500]}
