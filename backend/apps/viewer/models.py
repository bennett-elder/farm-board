from typing import Optional
from datetime import datetime, UTC
from pydantic import BaseModel, ConfigDict, Field


class PostModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "something-unique",
                "blurb": "Something to share",
                "date": "2014-02-10T10:50:42.000389",
            }
        },
    )

    id: str = Field(...)
    blurb: str = Field(...)
    date: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UpdatePostModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "blurb": "Something to share",
                "date": "2014-02-10T10:50:42.000389",
            }
        }
    )

    blurb: str = Field(...)
    date: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CommentModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "something-unique",
                "blurb": "Something to share",
                "date": "2014-02-10T10:50:42.000389",
            }
        },
    )

    id: str = Field(...)
    blurb: str = Field(...)
    date: datetime = Field(default_factory=lambda: datetime.now(UTC))
