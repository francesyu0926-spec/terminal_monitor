from __future__ import annotations

import httpx

from api_tests.core.http_client import ApiClient


class RestApi:
    """/terminal/rest 业务接口。"""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def info_column(self) -> httpx.Response:
        return self._client.get("/info/column")

    def info_detail(self, article_id: int) -> httpx.Response:
        return self._client.get("/info/detail", params={"id": article_id})

    def info_page(
        self,
        *,
        forward: bool = False,
        page_size: int = 20,
        subcat: int = 20,
    ) -> httpx.Response:
        return self._client.get(
            "/info/infoPage",
            params={"forward": forward, "pageSize": page_size, "subcat": subcat},
        )

    def hot_info(self) -> httpx.Response:
        return self._client.get("/hot/info")

    def monitor_scheme_view_list(self) -> httpx.Response:
        return self._client.get("/monitor/scheme/view/list")

    def monitor_scheme_view_detail(self, scheme_id: int) -> httpx.Response:
        return self._client.get(
            "/monitor/scheme/view/detail",
            params={"schemeId": scheme_id},
        )

    def monitor_group_search(
        self,
        *,
        scheme_id: int,
        relevance: str = '["0","1","2"]',
        emotion: str = '["0","1","2"]',
        page_no: int = 1,
        page_size: int = 10,
    ) -> httpx.Response:
        return self._client.post(
            "/monitor/group/search",
            json={
                "schemeId": scheme_id,
                "relevance": relevance,
                "emotion": emotion,
                "pageNo": page_no,
                "pageSize": page_size,
            },
        )

    def param_addr(self) -> httpx.Response:
        return self._client.get("/param/addr")

    def advertise_classify_list(self) -> httpx.Response:
        return self._client.get("/user/advertise/classify/list")

    def advertise_list(
        self,
        *,
        classify_id: int = 1,
        page_no: int = 1,
        page_size: int = 10,
    ) -> httpx.Response:
        return self._client.get(
            "/user/advertise/list",
            params={
                "classifyId": classify_id,
                "pageNo": page_no,
                "pageSize": page_size,
            },
        )

    def es_search_searchkey_page(
        self,
        *,
        category: int = 14,
        keyword: str = "",
        page_size: int = 20,
    ) -> httpx.Response:
        return self._client.get(
            "/esSearch/searchkey/page",
            params={"category": category, "keyword": keyword, "pageSize": page_size},
        )

    def organization_get_content_type(self) -> httpx.Response:
        return self._client.get("/organization/getContentType")

    def organization_report_detail(self, pid: int) -> httpx.Response:
        return self._client.get("/organization/reportDetail", params={"pid": pid})

    def company_notice_detail(self, notice_id: int) -> httpx.Response:
        return self._client.get("/company/notice/detail", params={"id": notice_id})

    def company_notice(
        self,
        *,
        page_no: int = 1,
        page_size: int = 20,
        start_date: str = "",
        end_date: str = "",
        secu_code: str = "",
        title: str = "",
        types: str = "",
    ) -> httpx.Response:
        return self._client.get(
            "/company/notice",
            params={
                "pageNo": page_no,
                "pageSize": page_size,
                "startDate": start_date,
                "endDate": end_date,
                "secuCode": secu_code,
                "title": title,
                "types": types,
            },
        )

    def article_flash(self, *, page_size: int = 8) -> httpx.Response:
        return self._client.get(
            "/article/flash",
            params={"pageSize": page_size},
        )

    def article_recent(self, *, forward: bool = False, page_size: int = 30) -> httpx.Response:
        return self._client.get(
            "/article/recent",
            params={"forward": forward, "pageSize": page_size},
        )

    def article_detail(self, catalog_id: int, article_id: int) -> httpx.Response:
        return self._client.get(f"/article/detail/{catalog_id}/{article_id}")

    def article_share_system_list(
        self,
        *,
        page_no: int = 1,
        page_size: int = 10,
    ) -> httpx.Response:
        return self._client.get(
            "/article/share/systemList",
            params={"pageNo": page_no, "pageSize": page_size},
        )

    def index_emotion(self) -> httpx.Response:
        return self._client.get("/index/emotion")

    def emotion_solution_view_list(self) -> httpx.Response:
        return self._client.get("/emotion/solution/view/list")

    def emotion_solution_q(
        self,
        *,
        match_all: bool = False,
        page_no: int = 1,
        page_size: int = 10,
        forward: bool = False,
        start_time: int = 1762272000000,
        end_time: int = 1793894399000,
        emotions: tuple[str, ...] = ("0", "1", "2"),
        markets: tuple[str, ...] = ("A", "HK", "US", "OTC", "B", "TW", "N"),
        tags: str = "[]",
        keywords: str = "",
        portfolio: str = "[]",
    ) -> httpx.Response:
        form: dict[str, str] = {
            "matchAll": str(match_all).lower(),
            "pageSize": str(page_size),
            "pageNo": str(page_no),
            "forward": str(forward).lower(),
            "startTime": str(start_time),
            "endTime": str(end_time),
            "tags": tags,
            "keywords": keywords,
            "portfolio": portfolio,
        }
        for index, value in enumerate(emotions):
            form[f"emotions[{index}]"] = value
        for index, value in enumerate(markets):
            form[f"markets[{index}]"] = value
        return self._client.post(
            "/emotion/solution/q",
            data=form,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    def index_trend(self, trend_id: int = 1) -> httpx.Response:
        return self._client.get(f"/index/trend/{trend_id}")

    def theme_recomend(self, *, theme_type: int = 2, page_size: int = 10) -> httpx.Response:
        return self._client.get(
            "/theme/recomend",
            params={"type": theme_type, "pageSize": page_size},
        )

    def theme_stock_articles(
        self,
        *,
        stock_code: str,
        page_no: int = 1,
        article_type: int = 1,
        page_size: int = 50,
    ) -> httpx.Response:
        return self._client.get(
            "/theme/stock/articles",
            params={
                "stockCode": stock_code,
                "pageNo": page_no,
                "type": article_type,
                "pageSize": page_size,
            },
        )

    def theme_fund_list(
        self,
        *,
        theme_id: int | None = None,
        page_size: int = 10,
    ) -> httpx.Response:
        params: dict[str, int | bool] = {"pageSize": page_size}
        if theme_id is not None:
            params["themeId"] = theme_id
        return self._client.get("/theme/fund/list", params=params)
