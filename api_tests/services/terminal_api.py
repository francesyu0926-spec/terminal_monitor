from __future__ import annotations

from typing import Any

import httpx

from api_tests.core.http_client import ApiClient


class TerminalApi:
    """终端监控 REST 封装，路径与后端约定保持一致时可复用。"""

    _collection = "/terminals"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def list(self, *, page: int = 1, page_size: int = 20) -> httpx.Response:
        return self._client.get(
            self._collection,
            params={"page": page, "page_size": page_size},
        )

    def get(self, terminal_id: str | int) -> httpx.Response:
        return self._client.get(f"{self._collection}/{terminal_id}")

    def create(self, payload: dict[str, Any]) -> httpx.Response:
        return self._client.post(self._collection, json=payload)

    def update(self, terminal_id: str | int, payload: dict[str, Any]) -> httpx.Response:
        return self._client.put(f"{self._collection}/{terminal_id}", json=payload)

    def delete(self, terminal_id: str | int) -> httpx.Response:
        return self._client.delete(f"{self._collection}/{terminal_id}")
