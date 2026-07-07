from fastapi import APIRouter, UploadFile
from infrastructure.langgraph_service import run_agent
from infrastructure.file_service import parse_doc
from domain.models.ask_request import AskRequest

router = APIRouter()


@router.post("/ask")
def ask(request: AskRequest):
    print(f"Received query: {request.query}")
    result = run_agent(request.query)
    print(f"Agent response: {result}")
    return result


@router.post("/upload_doc")
async def upload_doc(file: UploadFile):
    text = parse_doc(file)
    return {"parsed_text": text[:500]}
