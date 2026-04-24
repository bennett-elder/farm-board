from fastapi import FastAPI, Security, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader, APIKeyQuery
from fastapi.responses import JSONResponse, FileResponse
import os
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from apps.poster.routers import router as poster_router
from apps.viewer.routers import router as viewer_router

import api_security
import json

app = FastAPI()

if (settings.APP_MODE == "poster"):
    app.include_router(poster_router, tags=["posts"], prefix="/post",
            dependencies=[Depends(api_security.get_api_key)]
        )
elif (settings.APP_MODE == "viewer"):
    app.include_router(viewer_router, tags=["posts"], prefix="/post")
    app.mount("/assets", StaticFiles(directory=f"{settings.FRONTEND_BUILD_PATH}/assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        file_path = os.path.join(settings.FRONTEND_BUILD_PATH, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(f"{settings.FRONTEND_BUILD_PATH}/index.html")
elif (settings.APP_MODE == "dev"):
    # Serves both viewer (GET) and poster (POST) APIs without mounting static files.
    # Use with the frontend dev server (npm start).
    app.include_router(viewer_router, tags=["posts"], prefix="/post")
    app.include_router(poster_router, tags=["posts"], prefix="/post",
            dependencies=[Depends(api_security.get_api_key)]
        )

    @app.get("/config.json", include_in_schema=False)
    async def frontend_config():
        return JSONResponse({"customPostsName": settings.FRONTEND_POSTS_NAME})


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    if (settings.API_KEYS == 'USE TABLE'):
        key_collection=app.mongodb["api-keys"]
        cursor=key_collection.find()
        key_map={}
        for document in await cursor.to_list(length=10000):
            key_map[document["key"]] = document.get("poster_id")
        settings.API_KEYS = ','.join(key_map.keys())
        api_security.set_key_map(key_map)
    else:
        api_security.set_key_map({k.strip(): None for k in settings.API_KEYS.split(',')})
    if settings.APP_MODE != "dev":
        frontend_folder = settings.FRONTEND_BUILD_PATH
        replace_title_and_description(f'{frontend_folder}/index.html')
        replace_title_and_description(f'{frontend_folder}/manifest.json')
        write_frontend_config_file()

def replace_title_and_description(file_path):
    with open(file_path, "r+") as f:
        content = f.read()
        content = content.replace('__TITLE__', settings.FRONTEND_TITLE)
        content = content.replace('__SHORTNAME__', settings.FRONTEND_SHORTNAME)
        content = content.replace('__DESCRIPTION__', settings.FRONTEND_DESCRIPTION)
        f.seek(0)
        f.write(content)
        f.truncate()

def write_frontend_config_file():
    with open(f'{settings.FRONTEND_BUILD_PATH}/config.json', "w") as f:
        output = {}
        output["customPostsName"] = settings.FRONTEND_POSTS_NAME
        output_as_string = json.dumps(output)
        f.write(output_as_string)

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
