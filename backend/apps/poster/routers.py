from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import PostModel, UpdatePostModel
from datetime import datetime
import time

router = APIRouter()

@router.post("/", response_description="Add new post")
async def create_post_or_comment(request: Request, post: PostModel = Body(...)):
    now = datetime.utcnow()
    post = jsonable_encoder(post)
    post2 = {k: v for k, v in post.items() if v is not None}
    print('called post')
    print(post)
    print(post2)
    print(post["id"])
    id = post["id"]
    print(id)
    if (found_post := await request.app.mongodb["posts"].find_one({"id": id})) is not None:
        # found so update existing post
        update_post = {
            "blurb": post["blurb"],
            "date": now
        }
        update_result = await request.app.mongodb["posts"].update_one(
            {"id": id}, {"$set": update_post}
        )
    else:
        # post not found with matching id so create new one
        created_post_result = await request.app.mongodb["posts"].insert_one(post)
        created_post = await request.app.mongodb["posts"].find_one(
            {"_id": created_post_result.inserted_id}
        )

    # either way create a new comment record
    new_comment: UpdatePostModel = { 
        "id": post["id"],
        "blurb": post["blurb"],
        "date": now
    }
    new_comment_result = await request.app.mongodb["comments"].insert_one(
        new_comment
    )
    print(new_comment)
    created_comment = await request.app.mongodb["comments"].find_one(
        {"_id": new_comment_result.inserted_id}
    )
    created_comment['_id'] = str(created_comment['_id'])
    created_comment['date'] = int(time.mktime(created_comment['date'].timetuple())) * 1000
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_comment)
