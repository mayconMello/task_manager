import os
from pathlib import Path
from typing import Optional, Literal, List

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    ENVIRONMENT: Optional[Literal["development", "production", "test"]] = "development"

    ALLOWED_HOTS: List[str] = ["localhost", "testserver"]
    ALLOWED_ORIGINS: List[str] = ["http://localhost"]

    SECRET_KEY: str

    MEDIA_PATH: str = "media"
    MEDIA_URL: str = "media"

    MAX_FILE_SIZE_BYTES: int = 5 * 1024 * 1024

    DATABASE_URL: str
    DATABASE_URL_TEST: str = None

    JWT_EXPIRES_TOKEN_IN_MINUTES: int = 10
    JWT_EXPIRES_REFRESH_TOKEN_IN_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    EMAIL_HOST: str = None
    EMAIL_PORT: int = None
    EMAIL_HOST_USER: str = None
    EMAIL_HOST_PASSWORD: str = None

    BROKER_HOST: str
    BROKER_PORT: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        os.makedirs(self.storage_full_path, exist_ok=True)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.joinpath(".env"),
    )

    @computed_field
    @property
    def database(self) -> str:
        if self.ENVIRONMENT == "test":
            return self.DATABASE_URL_TEST

        return self.DATABASE_URL

    @computed_field
    @property
    def storage_full_path(self) -> Path:
        return BASE_DIR.joinpath(self.MEDIA_PATH)


settings = Settings()
