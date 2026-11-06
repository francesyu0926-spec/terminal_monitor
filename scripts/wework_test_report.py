"""解析 pytest JUnit，生成 PDF，并按参考模板推送企业微信（Markdown + PDF 文件）。"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx

# 测试函数 -> 接口展示名（与参考图「失败接口」一致：METHOD + 完整路径）
_DESK = "/terminal/desk/quotes/api"
_ENDPOINT_BY_TEST: dict[str, str] = {
    "test_login_returns_jwt_token": "POST /terminal/zxt-web/login/pwd",
    "test_token_provider_reuses_cached_token": "POST /terminal/zxt-web/login/pwd",
    "test_quotes_api_health": "GET /terminal/quotes/api/health",
    "test_quote_single_symbol": f"POST {_DESK}/quote",
    "test_line_chart": f"POST {_DESK}/line",
    "test_line5d_chart": f"POST {_DESK}/line5d",
    "test_catesorting_paged_list": f"POST {_DESK}/catesorting",
    "test_dayk_ohlc_series": f"POST {_DESK}/dayk",
    "test_weekk_ohlc_series": f"POST {_DESK}/weekk",
    "test_monthk_ohlc_series": f"POST {_DESK}/monthk",
    "test_yeark_ohlc_series": f"POST {_DESK}/yeark",
    "test_desk_intraday_ohlc_series": f"POST {_DESK}/{{interval}}",
    "test_desk_astocksquote": f"POST {_DESK}/astocksquote",
    "test_desk_sector_multiple_sort": f"POST {_DESK}/sectorMultipleSort",
    "test_desk_importantindex": f"POST {_DESK}/importantindex",
    "test_desk_profinmainindex": f"POST {_DESK}/profinmainindex",
    "test_desk_proincstatementnew": f"POST {_DESK}/proincstatementnew",
    "test_desk_probalsheetnew": f"POST {_DESK}/probalsheetnew",
    "test_desk_procfstatementnew": f"POST {_DESK}/procfstatementnew",
    "test_desk_subnewstockranking": f"POST {_DESK}/subnewstockranking",
    "test_desk_newsharescal": f"POST {_DESK}/newsharescal",
    "test_desk_search_v2": f"POST {_DESK}/search_v2",
    "test_info_column": "GET /terminal/rest/info/column",
    "test_info_page": "GET /terminal/rest/info/infoPage",
    "test_info_detail": "GET /terminal/rest/info/detail",
    "test_hot_info": "GET /terminal/rest/hot/info",
    "test_monitor_scheme_view_list": "GET /terminal/rest/monitor/scheme/view/list",
    "test_monitor_scheme_view_detail": "GET /terminal/rest/monitor/scheme/view/detail?schemeId={id}",
    "test_monitor_group_search": "POST /terminal/rest/monitor/group/search",
    "test_param_addr": "GET /terminal/rest/param/addr",
    "test_advertise_classify_list": "GET /terminal/rest/user/advertise/classify/list",
    "test_advertise_list": "GET /terminal/rest/user/advertise/list",
    "test_organization_get_content_type": "GET /terminal/rest/organization/getContentType",
    "test_organization_report_detail": "GET /terminal/rest/organization/reportDetail",
    "test_es_search_searchkey_page": "GET /terminal/rest/esSearch/searchkey/page",
    "test_company_notice": "GET /terminal/rest/company/notice",
    "test_company_notice_detail": "GET /terminal/rest/company/notice/detail",
    "test_article_flash_list": "GET /terminal/rest/article/flash",
    "test_article_recent_list": "GET /terminal/rest/article/recent",
    "test_article_detail": "GET /terminal/rest/article/detail/5/6493133",
    "test_article_share_system_list": "GET /terminal/rest/article/share/systemList",
    "test_index_emotion": "GET /terminal/rest/index/emotion",
    "test_emotion_solution_q": "POST /terminal/rest/emotion/solution/q",
    "test_emotion_solution_view_list": "GET /terminal/rest/emotion/solution/view/list",
    "test_index_trend_1": "GET /terminal/rest/index/trend/1",
    "test_theme_recomend_type2": "GET /terminal/rest/theme/recomend?type=2",
    "test_theme_recomend_type3": "GET /terminal/rest/theme/recomend?type=3",
    "test_theme_fund_list": "GET /terminal/rest/theme/fund/list",
    "test_theme_fund_list_by_theme_id": "GET /terminal/rest/theme/fund/list?themeId=13311271",
    "test_theme_stock_articles": "GET /terminal/rest/theme/stock/articles",
    "test_desk_quotes_page_loads": "GET /terminal/desk/quotes/",
    "test_zxt_desktop_news_detail_page_loads": "GET https://zxt.sfccn.com/desktop/news/details/1021804",
    "test_zxt_desktop_theme_index_page_loads": "GET https://zxt.sfccn.com/desktop/theme/index",
    "test_group_with_stocks_tree": "GET /terminal/quotes/user-stock/group/groupWithStocksTree",
    "test_banner_list": "GET /terminal/zxt-web/banner/list?position=4",
    "test_user_view_detail": "GET /terminal/zxt-web/user/view/detail",
    "test_user_market_guide": "GET /terminal/zxt-web/user/market/guide",
    "test_user_check_matketing_auth": "GET /terminal/zxt-web/user/checkMatketingAuth",
    "test_yqt_sso_token": "GET /terminal/zxt-web/yqt/ssoToken",
    "test_list_terminals": "GET /terminal/zxt-web/terminals",
    "test_mongo_view_themes": "GET /terminal/zxt-web/mongo/viewThemes",
    "test_mongo_view_details": "GET /terminal/zxt-web/mongo/viewDetails/{id}",
    "test_mongo_query": "POST /terminal/zxt-web/mongo/query",
    "test_laws_type_query": "GET /terminal/zxt-web/pubnote/lawsTypeQuery",
    "test_laws_query": "GET /terminal/zxt-web/pubnote/lawsQuery",
    "test_laws_detail": "GET /terminal/zxt-web/pubnote/lawsDetail",
    "test_meetinginvest_industries": "GET /terminal/zxt-web/meetinginvest/industries",
    "test_meetinginvest_page": "GET /terminal/zxt-web/meetinginvest/page",
    "test_overseas_report_realtime_search": "POST /terminal/zxt-web/overseasReport/realtime/search",
    "test_overseas_report_realtime_read": "GET /terminal/zxt-web/overseasReport/realtime/read",
}


@dataclass
class CaseResult:
    nodeid: str
    test_name: str
    outcome: str  # passed | failed | error | skipped
    message: str
    detail: str


@dataclass
class RunSummary:
    total: int
    passed: int
    failed: int
    errors: int
    skipped: int
    cases: list[CaseResult]

    @property
    def ok(self) -> bool:
        return self.failed == 0 and self.errors == 0


def _webhook_key(webhook_url: str) -> str:
    qs = parse_qs(urlparse(webhook_url).query)
    key = qs.get("key", [""])[0]
    if not key:
        raise ValueError("Webhook URL 中缺少 key 参数")
    return key


def send_markdown(webhook_url: str, content: str, *, verify_ssl: bool) -> None:
    resp = httpx.post(
        webhook_url,
        json={"msgtype": "markdown", "markdown": {"content": content}},
        timeout=30.0,
        verify=verify_ssl,
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("errcode", 0) != 0:
        raise RuntimeError(f"企业微信 Markdown 失败: {body}")


def upload_file(webhook_url: str, file_path: Path, *, verify_ssl: bool) -> str:
    key = _webhook_key(webhook_url)
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"
    with file_path.open("rb") as handle:
        resp = httpx.post(
            url,
            files={"media": (file_path.name, handle, "application/pdf")},
            timeout=60.0,
            verify=verify_ssl,
        )
    resp.raise_for_status()
    body = resp.json()
    if body.get("errcode", 0) != 0:
        raise RuntimeError(f"企业微信上传文件失败: {body}")
    media_id = body.get("media_id")
    if not media_id:
        raise RuntimeError(f"未返回 media_id: {body}")
    return str(media_id)


def send_file_message(webhook_url: str, media_id: str, *, verify_ssl: bool) -> None:
    resp = httpx.post(
        webhook_url,
        json={"msgtype": "file", "file": {"media_id": media_id}},
        timeout=30.0,
        verify=verify_ssl,
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("errcode", 0) != 0:
        raise RuntimeError(f"企业微信文件消息失败: {body}")


def testcase_nodeid(classname: str, name: str) -> str:
    if classname:
        module_path = classname.replace(".", "/") + ".py"
        return f"{module_path}::{name}"
    return name


def endpoint_label(test_name: str) -> str:
    base = test_name.split("[", 1)[0]
    label = _ENDPOINT_BY_TEST.get(base, base)
    if "[" in test_name and "{interval}" in label:
        param = test_name.split("[", 1)[1].rstrip("]")
        label = label.replace("{interval}", param)
    return label


def parse_junit(junit_path: Path) -> RunSummary:
    root = ET.parse(junit_path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))

    cases: list[CaseResult] = []
    total = passed = failed = errors = skipped = 0

    for suite in suites:
        total += int(suite.attrib.get("tests", 0))
        failed += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
        skipped += int(suite.attrib.get("skipped", 0))

        for case in suite.findall("testcase"):
            name = case.attrib.get("name", "")
            classname = case.attrib.get("classname", "")
            nodeid = testcase_nodeid(classname, name)

            if case.find("failure") is not None:
                el = case.find("failure")
                msg = (el.attrib.get("message") or "").strip()
                body = (el.text or "").strip()
                cases.append(
                    CaseResult(
                        nodeid=nodeid,
                        test_name=name,
                        outcome="failed",
                        message=msg,
                        detail=body,
                    )
                )
            elif case.find("error") is not None:
                el = case.find("error")
                msg = (el.attrib.get("message") or "").strip()
                body = (el.text or "").strip()
                cases.append(
                    CaseResult(
                        nodeid=nodeid,
                        test_name=name,
                        outcome="error",
                        message=msg,
                        detail=body,
                    )
                )
            elif case.find("skipped") is not None:
                cases.append(
                    CaseResult(
                        nodeid=nodeid,
                        test_name=name,
                        outcome="skipped",
                        message="",
                        detail="",
                    )
                )
            else:
                cases.append(
                    CaseResult(
                        nodeid=nodeid,
                        test_name=name,
                        outcome="passed",
                        message="",
                        detail="",
                    )
                )

    passed = total - failed - errors - skipped
    return RunSummary(total, passed, failed, errors, skipped, cases)


def build_markdown(
    summary: RunSummary,
    *,
    stamp: str,
    pdf_status: str | None = None,
) -> str:
    if summary.ok:
        verdict = '<font color="info">通过</font>'
    else:
        verdict = '<font color="warning">未通过</font>'

    lines = [
        "### 终端接口监控测试报告",
        f"> 时间：{stamp}",
        (
            f"> 结论：{verdict}（共 {summary.total} 条｜"
            f"通过 {summary.passed}｜失败 {summary.failed}｜"
            f"错误 {summary.errors}｜跳过 {summary.skipped}）"
        ),
    ]

    failed_endpoints: list[str] = []
    for case in summary.cases:
        if case.outcome in ("failed", "error"):
            failed_endpoints.append(endpoint_label(case.test_name))

    if failed_endpoints:
        lines.append("> 失败接口路径：")
        for ep in dict.fromkeys(failed_endpoints):
            lines.append(f"> - 接口路径：`{ep}`")

    if not summary.ok:
        if pdf_status == "pushed":
            lines.append("> 详细报告 PDF 已推送（本地副本见 reports/ 目录）")
        elif pdf_status == "gen_failed":
            lines.append("> 详细 PDF 未推送：生成失败，请查看 reports/ 下 HTML/JUnit 与 scheduled 日志")
        elif pdf_status == "upload_failed":
            lines.append("> 详细 PDF 未推送：企微上传失败，请查看服务器 reports/ 目录本地副本")
        else:
            lines.append("> 详细 PDF 未推送，请查看 reports/ 目录")
    return "\n".join(lines)


def _failure_context_text(case: CaseResult) -> str:
    return f"{case.message}\n{case.detail}"


def _trim_business_msg(raw: str) -> str:
    text = raw.strip().strip("'").strip('"').strip()
    return text[:400] if text else "（空）"


def _extract_business_response(case: CaseResult) -> tuple[str | None, str | None]:
    """从 JUnit 失败信息中解析接口 JSON 业务码与 msg/message（仅 PDF 使用）。"""
    blob = _failure_context_text(case)
    flat = re.sub(r"\s+", " ", blob)

    structured_patterns = (
        r"业务失败\s*code=([^\s]+)\s*msg=(.+?)(?=AssertionError|assert|$)",
        r"未登录\s*code=([^\s]+)\s*msg=(.+?)(?=AssertionError|assert|$)",
        r"登录业务失败:\s*code=([^\s]+)\s*msg=(.+?)(?=\||$)",
        r"业务失败\s*status=([^\s]+)\s*message=(.+?)(?=AssertionError|assert|$)",
        r"接口\s*code=([^\s]+)\s*msg=([^)）]+)",
    )
    for pat in structured_patterns:
        m = re.search(pat, flat, re.I)
        if m:
            return m.group(1).strip(), _trim_business_msg(m.group(2))

    json_patterns = (
        r"""['"]code['"]\s*:\s*([^,}\]]+).*?['"]msg['"]\s*:\s*['"]([^'"]*)['"]""",
        r"""['"]code['"]\s*:\s*([^,}\]]+).*?['"]message['"]\s*:\s*['"]([^'"]*)['"]""",
    )
    for pat in json_patterns:
        m = re.search(pat, blob, re.S | re.I)
        if m:
            code = m.group(1).strip()
            if code.lower() in ("null", "none"):
                continue
            return code, _trim_business_msg(m.group(2))

    return None, None


def _pdf_business_response_lines(case: CaseResult) -> list[str]:
    code, msg = _extract_business_response(case)
    if code is None and msg is None:
        return ["业务码：—", "返回信息：—"]
    return [
        f"业务码：{code if code is not None else '—'}",
        f"返回信息：{msg if msg is not None else '—'}",
    ]


def _pdf_phenomenon_line(case: CaseResult) -> str:
    """PDF 失败项：现象（单行）。"""
    blob = _failure_context_text(case)

    if re.search(r"\b404\b|Not Found", blob, re.I):
        return "现象：服务器提示「接口不存在」(HTTP 404)，当前环境无法访问该地址。"

    if "401" in blob or "未登录" in blob:
        return "现象：登录状态失效或未通过鉴权 (HTTP 401)。"

    if "5002" in blob or "开通权限" in blob:
        return "现象：账号暂无该功能权限。"

    if "应包含非空 content" in blob or ("content" in blob and "AssertionError" in blob):
        return "现象：接口有返回，但详情里缺少正文/关键内容字段。"

    if re.search(r"业务失败\s*code=", blob) or re.search(r"业务失败\s*status=", blob, re.I):
        return "现象：接口返回的业务状态未达到「成功」约定。"

    if "HTTP" in blob and re.search(r"HTTP\s*\d{3}", blob):
        status_m = re.search(r"HTTP\s*(\d{3})", blob)
        code = status_m.group(1) if status_m else "异常"
        return f"现象：HTTP 状态异常 ({code})，请求未按预期完成。"

    if "ConnectError" in blob or "EOF occurred" in blob:
        return "现象：网络或 TLS 连接异常，请求未能完成。"

    headline = _error_headline(case)
    cleaned = re.sub(r"^(AssertionError:\s*)+", "", headline).strip()
    if cleaned and len(cleaned) <= 200:
        return f"现象：{cleaned}"
    return "现象：自动化校验未通过，接口行为与预期不一致。"


def _error_headline(case: CaseResult) -> str:
    if case.message:
        one = re.sub(r"\s+", " ", case.message.replace("\r", "")).strip()
        if one:
            return one
    if case.detail:
        for line in case.detail.splitlines():
            line = line.strip()
            if line:
                return line
    return "未知错误"


def _pick_font() -> Path | None:
    candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\msyhbd.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
        Path("/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc"),
        Path("/usr/share/fonts/noto/NotoSansCJK-Regular.ttc"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def _pdf_set_font(pdf, font_path: Path | None, size: int) -> None:
    if font_path:
        pdf.set_font("report", size=size)
    else:
        pdf.set_font("Helvetica", size=size)


def _pdf_write(pdf, text: str, *, font_path: Path | None, size: int, line_h: float) -> None:
    from fpdf.enums import XPos, YPos

    _pdf_set_font(pdf, font_path, size)
    pdf.set_x(pdf.l_margin)
    content = (text or "").replace("\r", "")
    if not content.strip():
        content = " "
    # fpdf2：multi_cell(w=0) 结束后 x 会停在右缘，下一行可用宽度为 0
    pdf.multi_cell(pdf.epw, line_h, content, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def generate_pdf(
    summary: RunSummary,
    *,
    stamp: str,
    pdf_path: Path,
    html_report: Path | None,
    log_path: Path | None,
) -> None:
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = _pick_font()
    if font_path:
        pdf.add_font("report", "", str(font_path))
    _pdf_set_font(pdf, font_path, 14)

    failures = [c for c in summary.cases if c.outcome in ("failed", "error")]
    title = "终端接口监控测试报告-详细错误" if failures else "终端接口监控测试报告"
    pdf.cell(0, 9, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    _pdf_set_font(pdf, font_path, 11)
    pdf.cell(0, 7, f"时间: {stamp}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(
        0,
        7,
        (
            f"共{summary.total} 通过{summary.passed} 失败{summary.failed} "
            f"错误{summary.errors} 跳过{summary.skipped}"
        ),
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.ln(4)

    if not failures:
        _pdf_write(
            pdf,
            "本次巡检未发现失败或错误用例。",
            font_path=font_path,
            size=11,
            line_h=7,
        )
    else:
        _pdf_write(
            pdf,
            "以下为失败项（每项仅含：接口路径、业务码、返回信息、现象）。",
            font_path=font_path,
            size=10,
            line_h=6,
        )
        pdf.ln(2)
        failure_total = len(failures)
        for index, case in enumerate(failures, start=1):
            if index > 1:
                pdf.ln(3)
            _pdf_write(
                pdf,
                f"失败项 {index}/{failure_total}",
                font_path=font_path,
                size=12,
                line_h=7,
            )
            _pdf_write(
                pdf,
                f"接口路径：{endpoint_label(case.test_name)}",
                font_path=font_path,
                size=10,
                line_h=6,
            )
            for line in _pdf_business_response_lines(case):
                _pdf_write(pdf, line, font_path=font_path, size=10, line_h=6)
            _pdf_write(
                pdf,
                _pdf_phenomenon_line(case),
                font_path=font_path,
                size=10,
                line_h=6,
            )

    pdf.output(str(pdf_path))


def main() -> int:
    parser = argparse.ArgumentParser(description="企业微信测试报告（Markdown + PDF）")
    parser.add_argument("--webhook", required=True)
    parser.add_argument("--junit", required=True, type=Path)
    parser.add_argument(
        "--pdf-out",
        type=Path,
        default=None,
        help="失败时生成的 PDF 路径（通过时可省略）",
    )
    parser.add_argument("--stamp", default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    parser.add_argument("--html", type=Path, default=None)
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--insecure", action="store_true")
    args = parser.parse_args()
    verify_ssl = not args.insecure
    if not args.junit.exists():
        print(f"JUnit 不存在: {args.junit}", file=sys.stderr)
        return 1

    summary = parse_junit(args.junit)

    pdf_path: Path | None = None
    pdf_error: str | None = None
    if not summary.ok:
        pdf_path = args.pdf_out
        if pdf_path is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = args.junit.parent / f"wecom_failure_{ts}.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            generate_pdf(
                summary,
                stamp=args.stamp,
                pdf_path=pdf_path,
                html_report=args.html,
                log_path=args.log,
            )
        except Exception as exc:  # noqa: BLE001
            pdf_error = str(exc)
            pdf_path = None
            print(f"PDF 生成失败: {exc}", file=sys.stderr)

    pdf_uploaded = False
    pdf_upload_error: str | None = None
    if pdf_path is not None and pdf_path.is_file():
        try:
            media_id = upload_file(args.webhook, pdf_path, verify_ssl=verify_ssl)
            send_file_message(args.webhook, media_id, verify_ssl=verify_ssl)
            pdf_uploaded = True
        except Exception as exc:  # noqa: BLE001
            pdf_upload_error = str(exc)
            print(f"企业微信 PDF 推送失败: {exc}", file=sys.stderr)

    if pdf_uploaded:
        pdf_status = "pushed"
    elif pdf_error:
        pdf_status = "gen_failed"
    elif pdf_upload_error:
        pdf_status = "upload_failed"
    elif not summary.ok:
        pdf_status = "missing"
    else:
        pdf_status = None

    markdown = build_markdown(summary, stamp=args.stamp, pdf_status=pdf_status)
    try:
        send_markdown(args.webhook, markdown, verify_ssl=verify_ssl)
    except Exception as exc:  # noqa: BLE001
        print(f"企业微信 Markdown 推送失败: {exc}", file=sys.stderr)
        return 1

    if pdf_uploaded:
        print(f"已推送 Markdown + PDF: {pdf_path}")
    elif not summary.ok:
        print("已推送 Markdown（失败场景 PDF 未成功推送，见 stderr）", file=sys.stderr)
    else:
        print("已推送 Markdown（通过，未发送 PDF）")
    return 1 if (pdf_error or pdf_upload_error or (not summary.ok and not pdf_uploaded)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
