from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator

from .author import Author


class Reply(BaseModel):
    id: str
    kind: str
    author: Author

    deleted: bool
    content: str
    html_content: str = Field(alias="htmlContent")


class Comment(BaseModel):
    id: str
    kind: str
    author: Author

    deleted: bool
    content: str
    html_content: str = Field(alias="htmlContent")

    resolved: bool = Field(default=False)

    anchor: dict[str, float]

    replies: list[Reply] = Field(default=False)

    @field_validator("anchor", mode="before")
    def parse_boundaries(cls, v: str):
        # Regular expression to match the float numbers in the specific positions
        pattern = re.compile(r"\[\s*([\d.]+),([\d.]+),([\d.]+),([\d.]+)\s*\]")
        match = pattern.search(v)

        if not match:
            raise ValueError("String format is incorrect")

        # Extract the numbers from the match groups
        numbers = match.groups()
        left, top, right, bottom = [float(num) * 100 for num in numbers]

        return {"top": top, "left": left, "width": right - left, "height": bottom - top}
