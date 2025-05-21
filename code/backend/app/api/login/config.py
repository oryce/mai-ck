from urllib.parse import quote

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    KEYCLOAK_URL_INSIDE_DOCKER: str
    BASE_URL_KEYCLOAK: str
    REALM: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    BASE_URL_BACKEND: str

    @property
    def token_url(self) -> str:
        return f"{self.KEYCLOAK_URL_INSIDE_DOCKER}/realms/{self.REALM}/protocol/openid-connect/token"

    @property
    def auth_url(self) -> str:
        return (
            f"{self.BASE_URL_KEYCLOAK}/realms/{self.REALM}/protocol/openid-connect/auth"
        )

    @property
    def logout_url(self) -> str:
        return f"{self.KEYCLOAK_URL_INSIDE_DOCKER}/realms/{self.REALM}/protocol/openid-connect/logout"

    @property
    def userinfo_url(self) -> str:
        return f"{self.KEYCLOAK_URL_INSIDE_DOCKER}/realms/{self.REALM}/protocol/openid-connect/userinfo"

    @property
    def redirect_uri(self) -> str:
        return f"{self.BASE_URL_BACKEND}/login/callback"

    @property
    def encoded_redirect_uri(self) -> str:
        return quote(self.redirect_uri)

    model_config = SettingsConfigDict(env_file=f".env")


settings = Settings()
