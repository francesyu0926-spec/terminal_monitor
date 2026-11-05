from __future__ import annotations

from typing import Any, Mapping

import httpx

from api_tests.core.http_client import ApiClient


class ZxtWebApi:
    """/terminal/zxt-web 业务接口。"""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def banner_list(self, *, position: int | None = None) -> httpx.Response:
        params = {"position": position} if position is not None else None
        return self._client.get("/banner/list", params=params)

    def user_view_detail(self) -> httpx.Response:
        return self._client.get("/user/view/detail")

    def user_market_guide(self) -> httpx.Response:
        return self._client.get("/user/market/guide")

    def user_check_matketing_auth(self) -> httpx.Response:
        return self._client.get("/user/checkMatketingAuth")

    def yqt_sso_token(self) -> httpx.Response:
        return self._client.get("/yqt/ssoToken")

    def mongo_view_themes(self) -> httpx.Response:
        return self._client.get("/mongo/viewThemes")

    def mongo_view_details(self, view_id: int) -> httpx.Response:
        return self._client.get(f"/mongo/viewDetails/{view_id}")

    def mongo_query(
        self,
        payload: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        body: dict[str, Any] = {
            "collectionName": "BD_LC_SHARESTRU_2",
            "fields": [],
            "filters": {},
            "pagination": {"page": 1, "size": 10},
        }
        if payload is not None:
            body.update(payload)
        return self._client.post("/mongo/query", json=body)

    def meetinginvest_industries(self) -> httpx.Response:
        return self._client.get("/meetinginvest/industries")

    def meetinginvest_page(self, *, page_no: int = 1, page_size: int = 10) -> httpx.Response:
        return self._client.get(
            "/meetinginvest/page",
            params={"pageNo": page_no, "pageSize": page_size},
        )

    def laws_type_query(self) -> httpx.Response:
        return self._client.get("/pubnote/lawsTypeQuery")

    def laws_detail(self, seq: int) -> httpx.Response:
        return self._client.get("/pubnote/lawsDetail", params={"seq": seq})

    def laws_query(
        self,
        *,
        page_no: int = 1,
        page_size: int = 20,
        query_type: int = 1,
        key_word: str = "",
        laws_type: str = "",
    ) -> httpx.Response:
        return self._client.get(
            "/pubnote/lawsQuery",
            params={
                "pageNo": page_no,
                "pageSize": page_size,
                "type": query_type,
                "keyWord": key_word,
                "lawsType": laws_type,
            },
        )

    def overseas_report_realtime_search(
        self,
        payload: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        body: dict[str, Any] = {
            "languages": [],
            "institutions": [],
            "releaseDate": 0,
            "minPages": 0,
            "startDate": "",
            "endDate": "",
            "keyword": "",
            "pageNum": 1,
            "pageSize": 20,
        }
        if payload is not None:
            body.update(payload)
        return self._client.post("/overseasReport/realtime/search", json=body)

    def overseas_report_realtime_read(
        self,
        report_id: int,
        *,
        page_num: int = 1,
        page_size: int = 2,
    ) -> httpx.Response:
        return self._client.get(
            "/overseasReport/realtime/read",
            params={"id": report_id, "pageNum": page_num, "pageSize": page_size},
        )
