"""企业微信推送策略：指定时刻起仅在巡检失败时通知。"""

from __future__ import annotations

from datetime import datetime

from api_tests.config.settings import settings
from api_tests.core.quotes_call_window import _monitor_timezone


def _parse_cutoff(value: str) -> datetime:
    raw = value.strip()
    tz = _monitor_timezone()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            naive = datetime.strptime(raw, fmt)
            return naive.replace(tzinfo=tz)
        except ValueError:
            continue
    raise ValueError(f"无法解析 WEWORK_NOTIFY_FAILURE_ONLY_AFTER: {value!r}")


def failure_only_wecom_active(*, at: datetime | None = None) -> bool:
    """当前是否处于「仅失败推送企微」阶段（已过配置的起始时刻）。"""
    if not settings.wework_notify_failure_only_after.strip():
        return False
    cutoff = _parse_cutoff(settings.wework_notify_failure_only_after)
    tz = _monitor_timezone()
    moment = at.astimezone(tz) if at is not None else datetime.now(tz)
    return moment >= cutoff


def should_notify_wecom(*, run_ok: bool, at: datetime | None = None) -> bool:
    if not run_ok:
        return True
    if failure_only_wecom_active(at=at):
        return False
    return True
