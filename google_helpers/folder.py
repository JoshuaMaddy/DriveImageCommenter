from __future__ import annotations

from typing import TYPE_CHECKING

from google_helpers.file import get_all_files

from .models.file import File

if TYPE_CHECKING:
    from googleapiclient._apis.drive.v3 import DriveResource  # type: ignore


def get_all_root_folders(drive_service: DriveResource) -> list[File]:
    query = "mimeType = 'application/vnd.google-apps.folder'"
    folders = get_all_files(query=query, drive_service=drive_service)

    root_folders = list(filter(lambda x: x.parents is None, folders))

    return root_folders


def get_all_files_in_folder(folder_id: str, drive_service: DriveResource) -> list[File]:
    query = f"'{folder_id}' in parents"
    return get_all_files(query=query, drive_service=drive_service)


def get_folder(id: str, drive_service: DriveResource) -> File:
    file = drive_service.files().get(fileId=id).execute()
    return File.model_validate(file)


def get_parents(id: str, drive_service: DriveResource) -> list[File]:
    parent_ids: list[str] = (
        drive_service.files()
        .get(fileId=id, fields="parents")
        .execute()
        .get("parents", [])
    )

    parents: list[File] = []

    for parent_id in parent_ids:
        file = drive_service.files().get(fileId=parent_id).execute()
        parents.append(File.model_validate(file))

    return parents
