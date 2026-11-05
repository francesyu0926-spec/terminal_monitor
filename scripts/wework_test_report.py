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


def build_markdown(summary: RunSummary, *, stamp: str) -> str:
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
        lines.append("> 失败接口：")
        for ep in dict.fromkeys(failed_endpoints):
            lines.append(f"> - `{ep}`")

    if not summary.ok:
        lines.append("> 详细报告 PDF 已推送（本地副本见 reports/ 目录）")
    return "\n".join(lines)


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


def _error_body_lines(case: CaseResult) -> list[str]:
    raw = case.detail.replace("\r", "").strip()
    if not raw:
        return []
    lines = [ln.rstrip() for ln in raw.splitlines()]
    headline = _error_headline(case)
    if lines and re.sub(r"\s+", " ", lines[0].strip()) == re.sub(r"\s+", " ", headline):
        lines = lines[1:]
    cleaned: list[str] = []
    for line in lines:
        if not line.strip():
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        cleaned.append(line)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()
    return cleaned[:80]


def _pick_font() -> Path | None:
    candidates = [
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\msyhbd.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
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
    _pdf_set_font(pdf, font_path, size)
    pdf.multi_cell(0, line_h, text)


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
        for index, case in enumerate(failures, start=1):
            pdf.ln(2)
            _pdf_write(
                pdf,
                f"{index}. {endpoint_label(case.test_name)}",
                font_path=font_path,
                size=11,
                line_h=7,
            )
            _pdf_write(pdf, case.nodeid, font_path=font_path, size=11, line_h=7)
            _pdf_write(
                pdf,
                _error_headline(case),
                font_path=font_path,
                size=11,
                line_h=7,
            )
            for line in _error_body_lines(case):
                if line == "":
                    pdf.ln(3)
                    continue
                _pdf_write(pdf, line, font_path=font_path, size=10, line_h=6)

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
    markdown = build_markdown(summary, stamp=args.stamp)

    pdf_path: Path | None = None
    if not summary.ok:
        pdf_path = args.pdf_out
        if pdf_path is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = args.junit.parent / f"wecom_failure_{ts}.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        generate_pdf(
            summary,
            stamp=args.stamp,
            pdf_path=pdf_path,
            html_report=args.html,
            log_path=args.log,
        )

    try:
        if pdf_path is not None:
            media_id = upload_file(args.webhook, pdf_path, verify_ssl=verify_ssl)
            send_file_message(args.webhook, media_id, verify_ssl=verify_ssl)
        send_markdown(args.webhook, markdown, verify_ssl=verify_ssl)
    except Exception as exc:  # noqa: BLE001
        print(f"企业微信推送失败: {exc}", file=sys.stderr)
        return 1

    if pdf_path is not None:
        print(f"已推送 Markdown + PDF: {pdf_path}")
    else:
        print("已推送 Markdown（通过，未发送 PDF）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
