"""Асинхронный клиент Snov.io API.

Аутентификация: OAuth2 client_credentials -> Bearer access_token (живёт 3600 сек).

Пути эндпоинтов собраны в одном месте (класс Endpoints), чтобы их было легко
скорректировать под свой аккаунт. Помечено, что подтверждено, а что стоит
проверить на своём тарифе Snov.io (у разных планов набор методов отличается).
"""
from __future__ import annotations

import time
from typing import Any

import httpx

from .config import settings


class Endpoints:
    # Подтверждено (базовые методы, есть у всех тарифов с API):
    ACCESS_TOKEN = "/v1/oauth/access_token"
    USER_BALANCE = "/v1/get-balance"
    GET_LISTS = "/v1/get-user-lists"
    CREATE_LIST = "/v1/lists"
    ADD_PROSPECT = "/v1/add-prospect-to-list"
    GET_LIST_PROSPECTS = "/v1/prospect-list/{list_id}"

    # Drip-кампании (проверь доступность на своём тарифе):
    ADD_PROSPECT_TO_CAMPAIGN = "/v1/campaigns/{campaign_id}/prospects"
    CAMPAIGN_ANALYTICS = "/v1/get-campaign-analytics"


class SnovError(RuntimeError):
    pass


class SnovClient:
    def __init__(self) -> None:
        self.base = settings.snov_api_base.rstrip("/")
        self._token: str | None = None
        self._token_exp: float = 0.0

    # ---------- Аутентификация ----------
    async def _get_token(self, client: httpx.AsyncClient) -> str:
        if self._token and time.time() < self._token_exp - 60:
            return self._token
        if not settings.snov_ready:
            raise SnovError(
                "Не заданы SNOV_CLIENT_ID / SNOV_CLIENT_SECRET (см. .env)."
            )
        resp = await client.post(
            self.base + Endpoints.ACCESS_TOKEN,
            data={
                "grant_type": "client_credentials",
                "client_id": settings.snov_client_id,
                "client_secret": settings.snov_client_secret,
            },
        )
        if resp.status_code != 200:
            raise SnovError(f"Ошибка авторизации Snov.io ({resp.status_code}): {resp.text}")
        payload = resp.json()
        token = payload.get("access_token")
        if not token:
            raise SnovError(f"Snov.io не вернул access_token: {payload}")
        self._token = token
        self._token_exp = time.time() + int(payload.get("expires_in", 3600))
        return token

    # ---------- Низкоуровневый вызов ----------
    async def request(
        self, method: str, path: str, *, params: dict | None = None, data: dict | None = None
    ) -> Any:
        async with httpx.AsyncClient(timeout=30) as client:
            token = await self._get_token(client)
            headers = {"Authorization": f"Bearer {token}"}
            resp = await client.request(
                method,
                self.base + path,
                headers=headers,
                params=params,
                data=data,
            )
            if resp.status_code >= 400:
                raise SnovError(f"Snov.io {method} {path} -> {resp.status_code}: {resp.text}")
            try:
                return resp.json()
            except ValueError:
                return {"raw": resp.text}

    # ---------- Высокоуровневые методы ----------
    async def get_balance(self) -> Any:
        return await self.request("GET", Endpoints.USER_BALANCE)

    async def get_lists(self) -> Any:
        return await self.request("GET", Endpoints.GET_LISTS)

    async def create_list(self, name: str) -> Any:
        return await self.request("POST", Endpoints.CREATE_LIST, data={"name": name})

    async def add_prospect(self, list_id: int, prospect: dict) -> Any:
        data = {
            "listId": list_id,
            "email": prospect["email"],
            "firstName": prospect.get("first_name", ""),
            "lastName": prospect.get("last_name", ""),
            "fullName": (
                f"{prospect.get('first_name', '')} {prospect.get('last_name', '')}".strip()
            ),
            "companyName": prospect.get("company", ""),
            "position": prospect.get("position", ""),
        }
        return await self.request("POST", Endpoints.ADD_PROSPECT, data=data)

    async def add_prospect_to_campaign(self, campaign_id: int, prospect: dict) -> Any:
        path = Endpoints.ADD_PROSPECT_TO_CAMPAIGN.format(campaign_id=campaign_id)
        data = {
            "email": prospect["email"],
            "firstName": prospect.get("first_name", ""),
            "lastName": prospect.get("last_name", ""),
        }
        return await self.request("POST", path, data=data)

    async def campaign_analytics(self, campaign_id: int) -> Any:
        return await self.request(
            "GET", Endpoints.CAMPAIGN_ANALYTICS, params={"campaignId": campaign_id}
        )


snov_client = SnovClient()
