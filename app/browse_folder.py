from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from google_helpers.folder import File, get_all_files_in_folder, get_folder, get_parents

from .dependencies import Templates, create_drive_service_credentials

if TYPE_CHECKING:
    from googleapiclient._apis.drive.v3 import DriveResource  # type: ignore

router = APIRouter()


@router.get("/folder/{id}", response_class=HTMLResponse)
async def folder(request: Request, id: str, templates: Templates):
    drive_service: DriveResource = create_drive_service_credentials()
    unsorted_files = get_all_files_in_folder(folder_id=id, drive_service=drive_service)
    parents = get_parents(id=id, drive_service=drive_service)
    folder = get_folder(id=id, drive_service=drive_service)

    files: list[File] = []
    folders: list[File] = []

    for file in unsorted_files:
        if file.mimetype == "application/vnd.google-apps.folder":
            folders.append(file)
        else:
            files.append(file)

    sorted_files: list[File] = sorted(files, key=lambda file: file.name)
    sorted_folders: list[File] = sorted(folders, key=lambda file: file.name)

    return templates.TemplateResponse(
        request=request,
        name="folders.html",
        context={
            "request": request,
            "files": sorted_files,
            "folders": sorted_folders,
            "parents": parents,
            "folder": folder,
        },
    )
