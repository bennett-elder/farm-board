from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional

from .models import PostModel, UpdatePostModel
from datetime import datetime
import time
import api_security
from config import settings

router = APIRouter()

@router.post("/", response_description="Add new post")
async def create_post_or_comment(
    request: Request,
    post: PostModel = Body(...),
    poster_id_from_key: Optional[str] = Depends(api_security.get_poster_id),
):
    now = datetime.utcnow()
    post = jsonable_encoder(post)

    if poster_id_from_key is not None:
        id = poster_id_from_key
    elif settings.STRICT_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have an associated poster ID",
        )
    elif post.get("id"):
        # Deprecated: poster identifies itself via the POST body
        id = post["id"]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing poster ID",
        )

    post["id"] = id

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
        "id": id,
        "blurb": post["blurb"],
        "date": now
    }
    new_comment_result = await request.app.mongodb["comments"].insert_one(
        new_comment
    )
    created_comment = await request.app.mongodb["comments"].find_one(
        {"_id": new_comment_result.inserted_id}
    )
    created_comment['_id'] = str(created_comment['_id'])
    created_comment['date'] = int(time.mktime(created_comment['date'].timetuple())) * 1000
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_comment)
