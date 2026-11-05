from __future__ import annotations

import httpx

from api_tests.core.http_client import ApiClient


class UserStockApi:
    """/terminal/quotes/user-stock 自选分组等。"""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def group_with_stocks_tree(self) -> httpx.Response:
        return self._client.get("/user-stock/group/groupWithStocksTree")
