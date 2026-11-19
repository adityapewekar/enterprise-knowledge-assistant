from domain.ports import KnowledgeBase


class KnowledgeBaseService:
    def __init__(self, knowledge_base: KnowledgeBase):
        self._knowledge_base = knowledge_base

    def update_article(self, article: str, roles: list[str]) -> dict:
        return self._knowledge_base.update_article(article, roles)
