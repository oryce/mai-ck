from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    """
    PostgreSQL connection string.
    """
    pg_dsn: PostgresDsn

    """
    OpenID Connect issuer URI.
    """
    oidc_issuer: str
    
    oidc_audience: str
