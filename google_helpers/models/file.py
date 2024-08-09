from __future__ import annotations

from pydantic import BaseModel, Field


class File(BaseModel):
    kind: str
    mimetype: str = Field(alias="mimeType")
    id: str
    name: str
    parents: list[str] | None = Field(default=None)
