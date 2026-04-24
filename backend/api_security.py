from fastapi import HTTPException, status, Security, Depends
from fastapi.security import APIKeyHeader, APIKeyQuery
from typing import Optional
from config import settings

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# Maps validated key string → poster_id (None if the key has no associated poster)
_api_key_map: dict = {}


def set_key_map(key_map: dict):
    global _api_key_map
    _api_key_map = key_map


def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    """Retrieve and validate an API key from the query parameters or HTTP header.
        Based on https://joshdimella.com/blog/adding-api-key-auth-to-fast-api

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    API_KEYS = settings.API_KEYS
    print(API_KEYS)
    print(settings.API_KEYS)
    if api_key_query is None and api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )
    if api_key_query is not None and api_key_query in API_KEYS:
        return api_key_query
    if api_key_header is not None and api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )


def get_poster_id(
    api_key: str = Depends(get_api_key),
) -> Optional[str]:
    """Return the poster_id associated with the validated API key, or None if the key
    has no poster_id (legacy keys that rely on the POST body for identification)."""
    return _api_key_map.get(api_key)
