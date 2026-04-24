import os
os.environ.setdefault("API_KEYS", "legacy-key,poster-key")
os.environ.setdefault("DB_URL", "mongodb://localhost:27017")
os.environ.setdefault("DB_NAME", "testdb")

import pytest_asyncio
from fastapi import FastAPI, Depends
from httpx import AsyncClient, ASGITransport
import mongomock_motor

import api_security
from config import settings

LEGACY_KEY = "legacy-key"
POSTER_KEY = "poster-key"
POSTER_ID = "team-alpha"


@pytest_asyncio.fixture
async def app():
    settings.API_KEYS = f"{LEGACY_KEY},{POSTER_KEY}"
    settings.STRICT_API_KEYS = False
    api_security.set_key_map({
        LEGACY_KEY: None,
        POSTER_KEY: POSTER_ID,
    })

    from apps.poster.routers import router as poster_router
    test_app = FastAPI()
    test_app.include_router(
        poster_router,
        prefix="/post",
        dependencies=[Depends(api_security.get_api_key)],
    )
    test_app.mongodb = mongomock_motor.AsyncMongoMockClient()["testdb"]
    return test_app


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
