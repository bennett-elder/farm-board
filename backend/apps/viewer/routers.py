from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/", response_description="List all posts")
async def list_posts(request: Request):
    posts = []
    for doc in await request.app.mongodb["posts"].find({},{'_id': 0}).to_list(length=100):
        posts.append(doc)
    return posts


@router.get("/{id}", response_description="Get comment detail of a single post")
async def show_task(id: str, request: Request):
    if (post := await request.app.mongodb["posts"].find_one({"id": id})) is not None:
        comments = []
        for doc in await request.app.mongodb["comments"].find({"id": id},{'_id': 0}).to_list(length=100):
            comments.append(doc)
        return comments

    raise HTTPException(status_code=404, detail=f"Post {id} not found")

