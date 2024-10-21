import os
from pathlib import Path
from typing import Optional, Literal, List

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    environment: Optional[Literal['dev', 'prd', 'test']] = 'dev'

    allowed_hosts: List[str] = ['localhost', 'testserver']
    allowed_origins: List[str] = ['http://localhost']

    storage_path: str = 'media'
    storage_url: str = 'media'
    max_file_size_bytes: int = 5 * 1024 * 1024

    database_url: str
    database_url_test: str = None

    secret_key: str

    jwt_expires_token_in_minutes: int = 10
    jwt_expires_refresh_token_in_days: int = 7
    jwt_algorithm: str = 'HS256'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        os.makedirs(self.storage_full_path, exist_ok=True)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.joinpath('.env'),
    )

    @computed_field
    @property
    def database(self) -> str:
        if self.environment == 'test':
            return self.database_url_test

        return self.database_url

    @computed_field
    @property
    def storage_full_path(self) -> Path:
        return BASE_DIR.joinpath(self.storage_path)


settings = Settings()
