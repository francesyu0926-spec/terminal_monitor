from __future__ import annotations

from typing import Any, Mapping, MutableMapping

import httpx

from api_tests.auth.token_provider import TokenProvider
from api_tests.config.settings import settings
from api_tests.core.auth_headers import auth_headers_for_token
from api_tests.core.response import response_indicates_unauthorized
from api_tests.core.transport import httpx_verify


class ApiClient:
    """封装 httpx，统一 base URL、鉴权与超时。"""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
        headers: Mapping[str, str] | None = None,
        token_provider: TokenProvider | None = None,
    ) -> None:
        self._base_url = (base_url or settings.api_root).rstrip("/")
        self._timeout = timeout if timeout is not None else settings.timeout
        self._token_provider = token_provider
        default_headers: MutableMapping[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if headers:
            default_headers.update(headers)
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=self._timeout,
            headers=default_headers,
            verify=httpx_verify(),
        )

    def close(self) -> None:
        self._client.close()

    def _auth_headers(self) -> dict[str, str]:
        if self._token_provider is None and not settings.api_token:
            return {}
        token = self._token_provider.get_token() if self._token_provider else settings.api_token
        return auth_headers_for_token(token)

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any | None = None,
        data: Any | None = None,
        headers: Mapping[str, str] | None = None,
        retry_on_unauthorized: bool = True,
    ) -> httpx.Response:
        merged: MutableMapping[str, str] = {}
        merged.update(self._auth_headers())
        if headers:
            merged.update(headers)

        resp = self._client.request(
            method, url, params=params, json=json, data=data, headers=merged
        )
        if (
            retry_on_unauthorized
            and response_indicates_unauthorized(resp)
            and self._token_provider is not None
            and not settings.api_token
        ):
            self._token_provider.invalidate()
            merged.update(self._auth_headers())
            resp = self._client.request(
                method, url, params=params, json=json, data=data, headers=merged
            )
        return resp

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("PUT", url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> httpx.Response:
        return self.request("DELETE", url, **kwargs)
