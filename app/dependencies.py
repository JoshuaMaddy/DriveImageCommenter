from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore

from app_settings import Settings


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def templates() -> Jinja2Templates:
    return Jinja2Templates(directory="templates")


def create_drive_service_credentials(settings: Settings = get_settings()):
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    token_path = settings.credentials_folder / "token.json"
    credentials_path = settings.credentials_folder / "credentials.json"

    credentials = None

    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(  # type: ignore
            filename=str(token_path),
            scopes=SCOPES,
        )

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:  # type: ignore
            credentials.refresh(Request())  # type: ignore
        else:
            flow = InstalledAppFlow.from_client_secrets_file(  # type: ignore
                client_secrets_file=str(credentials_path),
                scopes=SCOPES,
            )
            credentials = flow.run_local_server(port=0)  # type: ignore

        with open(token_path, "w") as token:
            token.write(credentials.to_json())  # type: ignore

    return build("drive", "v3", credentials=credentials)


Templates = Annotated[Jinja2Templates, Depends(templates)]
