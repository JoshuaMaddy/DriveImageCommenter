from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    credentials_folder: Path = Path(__file__).parent / "credentials"
