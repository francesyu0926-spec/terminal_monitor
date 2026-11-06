"""`/terminal/quotes/api` 与 desk 行情 API 的可调用时段（默认 9:30–23:39，Asia/Shanghai）。"""

from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from api_tests.config.settings import settings


def _monitor_timezone() -> timezone | ZoneInfo:
    name = settings.quotes_api_call_timezone
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        if name in ("Asia/Shanghai", "PRC", "CST-8"):
            return timezone(timedelta(hours=8), name="Asia/Shanghai")
        raise


def _parse_hhmm(value: str) -> time:
    parts = value.strip().split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"时间格式应为 HH:MM: {value!r}")
    hour, minute = int(parts[0]), int(parts[1])
    return time(hour, minute)


def quotes_api_call_allowed(*, at: datetime | None = None) -> bool:
    if not settings.quotes_api_call_window_enabled:
        return True
    tz = _monitor_timezone()
    moment = at.astimezone(tz) if at is not None else datetime.now(tz)
    start = _parse_hhmm(settings.quotes_api_call_start)
    end = _parse_hhmm(settings.quotes_api_call_end)
    current = moment.time().replace(second=0, microsecond=0)
    end_inclusive = time(end.hour, end.minute, 59)
    return start <= current <= end_inclusive


def quotes_api_call_skip_reason() -> str:
    return (
        f"quotes/api 相关用例仅在 {settings.quotes_api_call_start}–{settings.quotes_api_call_end} "
        f"（{settings.quotes_api_call_timezone}）执行，当前时段跳过"
    )
