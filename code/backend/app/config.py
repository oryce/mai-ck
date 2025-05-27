from typing import Optional

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    """
    PostgreSQL connection string.
    """
    pg_dsn: PostgresDsn

    oidc_issuer_internal: str
    oidc_issuer_external: str
    oidc_audience: str

    redis_host: str
    redis_password: Optional[str]
