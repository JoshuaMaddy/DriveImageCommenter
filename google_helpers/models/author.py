from __future__ import annotations

from pydantic import BaseModel, Field


class Author(BaseModel):
    display_name: str = Field(alias="displayName")
    kind: str

    photo_link: str = Field(alias="photoLink")
