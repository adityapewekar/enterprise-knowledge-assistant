from fastapi import APIRouter

from application.services.knowledge_base_service import KnowledgeBaseService
from presentation.api.dependencies.services import get_knowledge_base_service
from presentation.api.request_dtos.kb_request_dto import KBRequestDto
from fastapi import Depends
from domain.document_errors import (
    DocumentExtractionError,
    KnowledgeBaseUnavailableError,
    MalformedDocumentError,
    UnsupportedDocumentTypeError,
)
from presentation.api.dependencies.services import get_document_service
from application.services.document_service import DocumentService
from fastapi import APIRouter, Depends, Form,  HTTPException, UploadFile
from presentation.api.dependencies.authentication import get_current_user

kb_router = APIRouter()

@kb_router.post("/update_kb_article")
def update(
    request: KBRequestDto,
    service: KnowledgeBaseService = Depends(get_knowledge_base_service),
):
    return service.update_article(request.article, request.roles)

@kb_router.post("/upload_doc", dependencies=[Depends(get_current_user)])
async def upload_doc(
    file: UploadFile,
    roles: list[str] = Form(default=[]),
    service: DocumentService = Depends(get_document_service),
):
    try:
        content = await file.read()
        text, indexed = service.ingest(file.filename or "", content, roles)
    except UnsupportedDocumentTypeError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except MalformedDocumentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (DocumentExtractionError, KnowledgeBaseUnavailableError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"parsed_text": text[:500], "indexed": indexed}
