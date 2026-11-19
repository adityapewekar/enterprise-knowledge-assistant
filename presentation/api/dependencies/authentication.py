import logging
import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientError

load_dotenv()

logger = logging.getLogger(__name__)
TENANT_ID = os.getenv("AZURE_TENANT_ID")
API_AUDIENCE = os.getenv("AZURE_API_AUDIENCE") or os.getenv("AZURE_CLIENT_ID")
JWKS_CLIENT = (
    PyJWKClient(f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys")
    if TENANT_ID
    else None
)
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Bearer access token is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not TENANT_ID or not API_AUDIENCE or JWKS_CLIENT is None:
        raise HTTPException(status_code=503, detail="Microsoft Entra API authentication is not configured.")
    try:
        signing_key = JWKS_CLIENT.get_signing_key_from_jwt(credentials.credentials)
        claims = jwt.decode(
            credentials.credentials,
            signing_key.key,
            algorithms=["RS256"],
            audience=API_AUDIENCE,
            issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
            options={"require": ["exp", "iss", "aud"]},
        )
    except (jwt.PyJWTError, PyJWKClientError) as exc:
        logger.warning("Microsoft Entra access-token validation failed: %s", exc)
        raise HTTPException(
            status_code=401,
            detail="Bearer access token is invalid or expired.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    scopes = claims.get("scp", "").split()
    tenant_id = claims.get("tid")
    object_id = claims.get("oid")
    if tenant_id != TENANT_ID or not object_id or "user.access" not in scopes:
        raise HTTPException(
            status_code=403,
            detail="Access token does not represent an authorized signed-in user.",
        )

    return f"{tenant_id}:{object_id}"
