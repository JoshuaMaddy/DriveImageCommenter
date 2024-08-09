from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from googleapiclient._apis.drive.v3 import DriveResource  # type: ignore


from googleapiclient.errors import HttpError
from httplib2 import HttpLib2Error

from .models.comment import Comment


def get_comments(id: str, drive_service: DriveResource) -> list[Comment]:
    comments: list[Comment] = []

    results = drive_service.comments().list(fileId=id, fields="*").execute()

    comments.extend(
        [Comment.model_validate(comment) for comment in results.get("comments", [])]
    )

    while next_page_token := results.get("nextPageToken", None):
        try:
            results = (
                drive_service.comments()
                .list(
                    pageToken=next_page_token,
                    fileId=id,
                    fields="*",
                )
                .execute()
            )
        except HttpError:
            print("Google related error occurred.")
            break
        except HttpLib2Error:
            print("Transport related error occurred.")
            break

        comments.extend(
            [Comment.model_validate(comment) for comment in results.get("comments", [])]
        )

    return comments
