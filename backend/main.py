from fastapi import FastAPI, Security, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader, APIKeyQuery
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from apps.poster.routers import router as poster_router
from apps.viewer.routers import router as viewer_router

import api_security

app = FastAPI()

if (settings.APP_MODE == "poster"):
    app.include_router(poster_router, tags=["posts"], prefix="/post",
            dependencies=[Depends(api_security.get_api_key)]
        )
elif (settings.APP_MODE == "viewer"):
    app.include_router(viewer_router, tags=["posts"], prefix="/post")
    app.mount("/", StaticFiles(directory="../frontend/build",html = True), name="static")


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
