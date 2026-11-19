from domain.document_errors import KnowledgeBaseUnavailableError
from domain.ports import DocumentParser, KnowledgeBase


class DocumentService:
    def __init__(self, parser: DocumentParser, knowledge_base: KnowledgeBase):
        self._parser = parser
        self._knowledge_base = knowledge_base

    def parse(self, filename: str, content: bytes) -> str:
        return self._parser.parse(filename, content)

    def ingest(self, filename: str, content: bytes, roles: list[str]) -> tuple[str, bool]:
        text = self.parse(filename, content)
        if not text.strip():
            return text, False

        result = self._knowledge_base.update_article(text, roles)
        if not result.get("success"):
            raise KnowledgeBaseUnavailableError(result.get("message", "The knowledge base could not index the upload."))
        return text, True
