from os.path import join
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = (
    'settings',
)


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    model_config = SettingsConfigDict(
        env_file=join(Path(__file__).resolve().parent.parent.parent, '.env'),
        env_file_encoding='utf-8',
    )


settings = Settings()
