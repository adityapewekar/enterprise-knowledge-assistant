import json

from domain.ports import AgentPort
from application.services.conversation_service import ConversationService


class AskService:
    def __init__(self, agent: AgentPort, conversations: ConversationService):
        self._agent = agent
        self._conversations = conversations

    def ask(self, user_id: str, query: str, role: str) -> dict:
        history = self._conversations.get_context_messages(user_id)
        result = self._agent.run(query, role, history)
        if not isinstance(result, dict):
            result = {"response": str(result)}

        if "error" not in result:
            answer = result.get("response") or result.get("message")
            if not isinstance(answer, str):
                answer = str(answer) if answer is not None else json.dumps(result, ensure_ascii=False)
            result["response"] = answer
            self._conversations.save_exchange(user_id, query, answer)

        return result
