from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class PostModel(BaseModel):
    id: str = Field(...)
    blurb: str = Field(...)
    date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "something-unique",
                "blurb": "Something to share",
                "date" : datetime(2014, 2, 10, 10, 50, 42, 389),
            }
        }

class UpdatePostModel(BaseModel):
    blurb: str = Field(...)
    date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "blurb": "Something to share",
                "date" : datetime(2014, 2, 10, 10, 50, 42, 389),
            }
        }

class CommentModel(BaseModel):
    id: str = Field(...)
    blurb: str = Field(...)
    date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "something-unique",
                "blurb": "Something to share",
                "date" : datetime(2014, 2, 10, 10, 50, 42, 389)
            }
        }