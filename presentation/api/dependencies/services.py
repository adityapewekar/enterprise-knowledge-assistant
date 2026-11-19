from functools import lru_cache

from application.services.ask_service import AskService
from application.services.conversation_service import ConversationService
from application.services.document_service import DocumentService
from application.services.knowledge_base_service import KnowledgeBaseService
from infrastructure.db.sqlite.conversation_db_service import SqliteConversationRepository
from infrastructure.db.vector.chroma_db_service import ChromaKnowledgeBase
from infrastructure.file_service import MultiFormatDocumentParser
from infrastructure.langgraph_service import LangGraphAgent


def get_conversation_service() -> ConversationService:
    return ConversationService(SqliteConversationRepository())


def get_ask_service() -> AskService:
    return AskService(LangGraphAgent(), get_conversation_service())


def get_knowledge_base_adapter() -> ChromaKnowledgeBase:
    return ChromaKnowledgeBase()


def get_document_service() -> DocumentService:
    return DocumentService(MultiFormatDocumentParser(), get_knowledge_base_adapter())


def get_knowledge_base_service() -> KnowledgeBaseService:
    return KnowledgeBaseService(get_knowledge_base_adapter())
