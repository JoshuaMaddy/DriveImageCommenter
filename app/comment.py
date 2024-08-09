from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from fastapi import APIRouter, Request

from google_helpers.models.comment import Comment, Reply

from .dependencies import Templates, create_drive_service_credentials

if TYPE_CHECKING:
    from googleapiclient._apis.drive.v3 import DriveResource  # type: ignore

router = APIRouter()


@dataclass
class NewComment:
    top: str
    left: str
    width: str
    height: str
    content: str
    id: str


@dataclass
class NewReply:
    content: str
    file_id: str
    comment_id: str


@router.post("/comment")
async def comment(
    request: Request,
    new_comment: NewComment,
    templates: Templates,
):
    drive_service: DriveResource = create_drive_service_credentials()

    left = float(new_comment.left[:-1]) / 100
    top = float(new_comment.top[:-1]) / 100
    width = float(new_comment.width[:-1]) / 100
    height = float(new_comment.height[:-1]) / 100

    right = left + width
    bottom = top + height

    response = (
        drive_service.comments()
        .create(
            fileId=new_comment.id,
            body={
                "anchor": f'[null,[null,[{left},{top},{right},{bottom}]],null,"head"]',
                "content": new_comment.content,
            },
            fields="*",
        )
        .execute()
    )

    return templates.TemplateResponse(
        request=request,
        name="comment.html",
        context={
            "request": request,
            "comment": Comment.model_validate(response),
        },
    )


@router.post("/reply")
async def reply(
    request: Request,
    new_reply: NewReply,
    templates: Templates,
):
    drive_service: DriveResource = create_drive_service_credentials()

    response = (
        drive_service.replies()
        .create(
            fileId=new_reply.file_id,
            commentId=new_reply.comment_id,
            body={
                "content": new_reply.content,
            },
            fields="*",
        )
        .execute()
    )

    return templates.TemplateResponse(
        request=request,
        name="reply.html",
        context={
            "request": request,
            "reply": Reply.model_validate(response),
        },
    )
