from typing import Any, Optional

from cachetools import TTLCache
from fastapi import HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OpenIdConnect,
    SecurityScopes,
)
from httpx import AsyncClient
from jose import JWTError, jwt
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from .config import Settings


class AccessTokenCredentials(HTTPAuthorizationCredentials):
    token: dict[str, Any]


class AccessTokenValidator(HTTPBearer):
    """
    Generic HTTPBearer Validator that validates JWT tokens given the JWKS provided at jwks_url.

    Source: https://github.com/fastapi/fastapi/pull/10278.
    """

    def __init__(
        self,
        *,
        jwks_url: str,
        audience: str,
        issuer: str,
        expire_seconds: int = 3600,
        roles_claim: str = "groups",
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(scheme_name=scheme_name, description=description)

        self.uri = jwks_url
        self.audience = audience
        self.issuer = issuer
        self.roles_claim = roles_claim
        self.keyset_cache: TTLCache[str, str] = TTLCache(16, expire_seconds)

    async def get_jwt_keyset(self) -> str:
        """
        Retrieves keyset when expired/not cached yet.
        """

        result: Optional[str] = self.keyset_cache.get(self.uri)

        if result is None:
            async with AsyncClient() as client:
                response = await client.get(self.uri)
                result = self.keyset_cache[self.uri] = response.text

        return result

    async def __call__(
        self, request: Request, security_scopes: SecurityScopes
    ) -> AccessTokenCredentials:  # type: ignore
        """
        Validates the JWT Access Token.

        If security_scopes are given, they are validated against the roles_claim in the Access Token.
        """

        # 1. Unpack bearer token
        unverified_token = await super().__call__(request)

        if not unverified_token:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid Access Token")

        access_token = unverified_token.credentials

        try:
            # 2. Get keyset from authorization server so that we can validate the JWT Access Token
            keyset = await self.get_jwt_keyset()

            # 3. Perform validation
            verified_token = jwt.decode(
                token=access_token,
                key=keyset,
                audience=self.audience,
                issuer=self.issuer,
                # The frontend doesn't provide an access token.
                options={"verify_at_hash": False},
            )
        except JWTError:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="JWT authentication failed",
            ) from None

        # 4. if security scopes are present, validate them
        if security_scopes and security_scopes.scopes:
            # 4.1 the roles_claim must be present in the access token
            scopes = verified_token.get(self.roles_claim)

            if scopes is None:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST, detail="Unsupported Access Token"
                )

            # 4.2 all required roles in the roles_claim must be present
            if not set(security_scopes.scopes).issubset(set(scopes)):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not Authorized"
                )

        return AccessTokenCredentials(
            scheme=self.scheme_name, credentials=access_token, token=verified_token
        )


settings = Settings()

jwks_url = f"{settings.oidc_issuer_internal}/protocol/openid-connect/certs"
oidc_url = f"{settings.oidc_issuer_internal}/.well-known/openid-configuration"

# Don't know what `client_id` should be set to

# swagger_ui_init_oauth = {
#     "clientId": settings.client_id,
#     "scopes": ["openid"],  # fill in additional scopes when necessary
#     "appName": "Test Application",
#     "usePkceWithAuthorizationCodeGrant": True,
# }

oidc = OpenIdConnect(openIdConnectUrl=oidc_url)

oauth2 = AccessTokenValidator(
    jwks_url=jwks_url, audience=settings.oidc_audience, issuer=settings.oidc_issuer_external
)
