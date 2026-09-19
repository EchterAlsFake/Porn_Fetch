"""Minimal asynchronous client for the PocketBase REST API."""
from __future__ import annotations

import asyncio
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .errors import PocketBaseError


class PocketBaseClient:
    """Small async client for the PocketBase endpoints used by this application."""

    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token = ""

    async def authenticate(self, email: str, password: str) -> None:
        response = await self.request(
            "POST",
            "/api/collections/_superusers/auth-with-password",
            {"identity": email, "password": password},
            authenticated=False,
        )
        self.token = str(response["token"])

    async def request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        *,
        query: dict[str, Any] | None = None,
        authenticated: bool = True,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self._request_sync, method, path, body, query, authenticated
        )

    def _request_sync(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None,
        query: dict[str, Any] | None,
        authenticated: bool,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        encoded_body = None
        headers = {"Accept": "application/json"}
        if body is not None:
            encoded_body = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if authenticated and self.token:
            headers["Authorization"] = self.token

        request = Request(url, data=encoded_body, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = response.read()
        except HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            raise PocketBaseError(
                f"PocketBase returned HTTP {error.code} for {method} {path}: {details}"
            ) from error
        except (OSError, URLError) as error:
            raise PocketBaseError(f"PocketBase request failed for {method} {path}: {error}") from error
        if not payload:
            return {}
        try:
            return json.loads(payload)
        except json.JSONDecodeError as error:
            raise PocketBaseError(f"PocketBase returned invalid JSON for {method} {path}") from error

    async def list_records(
        self, collection: str, *, filter_expression: str = "", sort: str = ""
    ) -> list[dict[str, Any]]:
        page = 1
        records: list[dict[str, Any]] = []
        while True:
            query: dict[str, Any] = {"page": page, "perPage": 500}
            if filter_expression:
                query["filter"] = filter_expression
            if sort:
                query["sort"] = sort
            response = await self.request(
                "GET", f"/api/collections/{collection}/records", query=query
            )
            records.extend(response.get("items", []))
            if page >= int(response.get("totalPages", 1)):
                return records
            page += 1

    async def find_by_url(self, collection: str, url: str) -> dict[str, Any] | None:
        quoted_url = json.dumps(url, ensure_ascii=False)
        records = await self.list_records(collection, filter_expression=f"url = {quoted_url}")
        return records[0] if records else None

    async def create_record(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self.request("POST", f"/api/collections/{collection}/records", data)

    async def update_record(
        self, collection: str, record_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.request(
            "PATCH", f"/api/collections/{collection}/records/{record_id}", data
        )
