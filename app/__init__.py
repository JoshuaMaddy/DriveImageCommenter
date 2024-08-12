from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from google_helpers.folder import get_all_root_folders, get_shared_with_me

from . import browse_folder, comment, image
from .dependencies import Templates, create_drive_service_credentials

app = FastAPI()

app.include_router(browse_folder.router)
app.include_router(image.router)
app.include_router(comment.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request, templates: Templates):
    drive_service = drive_service = create_drive_service_credentials()
    folders = get_all_root_folders(drive_service=drive_service)
    shared_folders = get_shared_with_me(drive_service=drive_service)

    return templates.TemplateResponse(
        request=request,
        name="folders.html",
        context={
            "request": request,
            "folders": folders,
            "shared_folders": shared_folders,
        },
    )
