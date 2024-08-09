from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, StreamingResponse

from google_helpers.comment import get_comments
from google_helpers.file import get_media

from .dependencies import Templates, create_drive_service_credentials

if TYPE_CHECKING:
    from googleapiclient._apis.drive.v3 import DriveResource  # type: ignore

router = APIRouter()


@router.get("/image/{id}", response_class=HTMLResponse)
async def image(
    request: Request,
    id: str,
    templates: Templates,
    folder_id: str | None = None,
):
    drive_service: DriveResource = create_drive_service_credentials()
    comments = get_comments(id=id, drive_service=drive_service)

    filtered_comments = []
    for comment in comments:
        if comment.deleted or comment.resolved:
            continue
        else:
            filtered_comments.append(comment)

    sorted_comments = sorted(filtered_comments, key=lambda x: x.id)  # type: ignore

    return templates.TemplateResponse(
        request=request,
        name="image.html",
        context={
            "request": request,
            "comments": sorted_comments,
            "folder_id": folder_id,
            "id": id,
        },
    )


@router.get("/image_media/{id}", response_class=StreamingResponse)
async def image_media(request: Request, id: str):
    drive_service: DriveResource = create_drive_service_credentials()
    media = get_media(id=id, drive_service=drive_service)

    return StreamingResponse(content=media, media_type="image")
