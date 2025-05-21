import os
import httpx
from fastapi.responses import RedirectResponse
from fastapi import APIRouter

router = APIRouter(tags=["login"])
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM_NAME = os.getenv("KEYCLOAK_REALM")
CLIENT_ID = os.getenv("KEYCLOAK_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_SECRET")


async def get_access_token():
    url = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
    print(f"Requesting token from: {url}")
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        response.raise_for_status()
        return response.json()['access_token']


async def get_identity_providers(access_token):
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/identity-provider/instances"
    print(f"Requesting identity providers from: {url}")
    headers = {'Authorization': f'Bearer {access_token}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        response.raise_for_status()
        return response.json()


@router.get("/auth/providers")
async def get_providers():
    providers = [
        {
            "id": "keycloak",
            "name": "Keycloak",
            "type": "oauth",
            "authorizationUrl": f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/auth",
            "tokenUrl": f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token",
            "clientId": CLIENT_ID,
            "clientSecret": CLIENT_SECRET,
            "redirectUri": "http://your-app.com/callback",
            "scope": "openid profile email",
            "responseType": "code",
            "state": "randomStateString"
        }]
    return {"providers": providers}


@router.get("/auth/signin")
async def signin(callbackUrl: str = "/"):
    return RedirectResponse(
        f"http://localhost:8080/realms/{REALM_NAME}/protocol/openid-connect/auth"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&scope=openid"
        f"&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Flogin%2Fcallback"
    )


@router.get("/login/callback", include_in_schema=False)
async def login_callback(
        code: str | None = None,
        error: str | None = None,
        error_description: str | None = None
) -> RedirectResponse:
    pass
