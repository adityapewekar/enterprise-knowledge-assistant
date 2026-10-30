from fastapi import APIRouter

from infrastructure.token_service import MAX_RESPONSE_TOKENS


token_router = APIRouter()


@token_router.get("/token/limits")
def get_token_limits():
    return {
        "max_response_tokens": MAX_RESPONSE_TOKENS,
        "status": "ok"
    }


@token_router.get("/token/health")
def token_health():
    return {"status": "ok"}
