from functools import lru_cache
import os

from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from domain.document_errors import DocumentExtractionError


@lru_cache(maxsize=10)
def get_kv_secret(secret_name: str) -> str:
    env_value = os.getenv(secret_name)
    if env_value:
        return env_value

    vault_url = os.getenv("AZURE_KEYVAULT_URL", "").strip()
    if not vault_url:
        return ""

    try:
        tenant_id = os.getenv("AZURE_TENANT_ID")
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")

        credential = (
            ClientSecretCredential(tenant_id, client_id, client_secret)
            if tenant_id and client_id and client_secret
            else DefaultAzureCredential()
        )
        client = SecretClient(vault_url=vault_url, credential=credential)
        secret = client.get_secret(secret_name)
        return secret.value or ""
    except Exception:
        return ""
    

def get_content_from_di(content: bytes)-> str:
        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
        if not endpoint or not key:
            raise DocumentExtractionError(
                "Azure AI Document Intelligence OCR is not configured."
            )

        try:
            client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
            poller = client.begin_analyze_document(
                "prebuilt-read",
                body=content,
                content_type="application/octet-stream",
            )
            result = poller.result()
            return result.content or ""
        except Exception as exc:
            print(f"Error during Azure Document Intelligence OCR: {exc}")
            raise DocumentExtractionError(
                "Azure AI Document Intelligence OCR is unavailable or failed to process the image."
            ) from exc
