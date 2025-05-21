import os
import httpx

# from fastapi_keycloak import FastAPIKeycloak
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["login"])
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
REALM_NAME = os.getenv("KEYCLOAK_REALM")
CLIENT_ID = os.getenv("KEYCLOAK_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_SECRET")

# Function to get the access token using client credentials flow
async def get_access_token():
    url = f"{KEYCLOAK_URL}/realms/{REALM_NAME}/protocol/openid-connect/token"
    print(f"Requesting token from: {url}")  # Печатаем полный URL
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        print(f"Response status: {response.status_code}")  # Печатаем статус ответа
        print(f"Response body: {response.text}")  # Печатаем тело ответа для отладки
        response.raise_for_status()  # Если есть ошибка, будет выброшено исключение
        return response.json()['access_token']  # Извлекаем access_token

async def get_identity_providers(access_token):
    url = f"{KEYCLOAK_URL}/admin/realms/{REALM_NAME}/identity-provider/instances"
    print(f"Requesting identity providers from: {url}")  # Печатаем полный URL
    headers = {'Authorization': f'Bearer {access_token}'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        print(f"Response status: {response.status_code}")  # Печатаем статус ответа
        print(f"Response body: {response.text}")  # Печатаем тело ответа для отладки
        response.raise_for_status()  # Если есть ошибка, будет выброшено исключение
        return response.json()  # Возвращаем список провайдеров


@router.get("/auth/providers")
async def get_providers():
    try:
        # Step 1: Get the access token
        access_token = await get_access_token()
        print("accesss token got")
        # Step 2: Get the identity providers from Keycloak
        providers = await get_identity_providers(access_token)

        # Step 3: Return the identity providers as a JSON response
        return {"providers": providers}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error fetching identity providers")
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))