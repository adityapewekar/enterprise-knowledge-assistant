from fastapi import APIRouter

from infrastructure.chroma_db_service import update_kb_article
from presentation.api.request_dtos.kb_request_dto import KBRequestDto

kb_router = APIRouter()

@kb_router.post("/update_kb_article")
def update(request:KBRequestDto):
    return update_kb_article(request)