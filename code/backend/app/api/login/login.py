import os
import httpx
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.login.keycloak_client import KeycloakClient
from app.api.login.auth_dep import get_current_user, get_keycloak_client
from app.api.login.config import settings

router = APIRouter(tags=["login"])

@router.get("/auth/providers")
async def get_providers():
    providers = [
        {
            "id": "keycloak",
            "name": "Keycloak",
            "type": "oauth",
            "authorizationUrl": settings.auth_url,
            "tokenUrl": settings.token_url,
            "clientId": settings.CLIENT_ID,
            "clientSecret": settings.CLIENT_SECRET,
            "redirectUri": settings.encoded_redirect_uri
        }]
    return {"providers": providers}


@router.get("/auth/signin")
async def signin(callbackUrl: str = "/"):
    return RedirectResponse(
        f"{settings.auth_url}"
        f"?client_id={settings.CLIENT_ID}"
        f"&response_type=code"
        f"&scope=openid"
        f"&redirect_uri={settings.encoded_redirect_uri}"
    )


@router.get("/login/callback", include_in_schema=False)
async def login_callback(
        code: str | None = None,
        error: str | None = None,
        error_description: str | None = None,
        keycloak: KeycloakClient = Depends(get_keycloak_client),
) -> RedirectResponse:
    """
    Обрабатывает callback после авторизации в Keycloak.
    Получает токен, информацию о пользователе, сохраняет пользователя в БД (если нужно)
    и устанавливает cookie с токенами. Обрабатывает ошибки от Keycloak.
    """
    if error:
        raise HTTPException(status_code=401, detail="Authorization code is required")

    if not code:
        raise HTTPException(status_code=401, detail="Authorization code is required")

    try:
        # Получение токенов от Keycloak
        token_data = await keycloak.get_tokens(code)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        id_token = token_data.get("id_token")

        if not access_token:
            raise HTTPException(status_code=401, detail="Токен доступа не найден")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token не найден")
        if not id_token:
            raise HTTPException(status_code=401, detail="ID token не найден")

        # Получение информации о пользователе
        user_info = await keycloak.get_user_info(access_token)
        user_id = user_info.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="ID пользователя не найден")

        # Установка cookie с токенами и редирект
        response = RedirectResponse(url="/protected")
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            path="/",
            max_age=token_data.get("expires_in", 3600),
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            path="/",
            max_age=token_data.get("refresh_expires_in", 2592000),
        )
        response.set_cookie(
            key="id_token",
            value=id_token,
            httponly=True,
            secure=True,
            samesite="lax",
            path="/",
            max_age=token_data.get("expires_in", 3600),
        )
        return response

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=401, detail="Ошибка авторизации")
