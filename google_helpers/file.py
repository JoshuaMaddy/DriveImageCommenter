from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from googleapiclient._apis.drive.v3 import DriveResource  # type: ignore


from .models.file import File


def get_all_files(query: str, drive_service: DriveResource) -> list[File]:
    files: list[File] = []

    results = (
        drive_service.files()
        .list(q=query, fields="files(kind, mimeType, id, name, parents)")
        .execute()
    )

    if "files" in results.keys():
        files.extend([File.model_validate(file) for file in results.get("files")])  # type: ignore

    while next_page_token := results.get("nextPageToken"):
        results = (
            drive_service.files()
            .list(
                pageToken=next_page_token,
                q=query,
            )
            .execute()
        )

        if "files" in results.keys():
            files.extend([File.model_validate(file) for file in results.get("files")])  # type: ignore

    return files


def get_media(id: str, drive_service: DriveResource) -> BytesIO:
    media = drive_service.files().get_media(fileId=id).execute()

    return BytesIO(media)
