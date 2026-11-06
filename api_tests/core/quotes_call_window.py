"""`/terminal/quotes/api` 与 desk 行情 API 的可调用时段（见 config/monitor_policy.json）。"""

from __future__ import annotations

from datetime import datetime, time

from api_tests.config.monitor_policy import load_monitor_policy, monitor_timezone


def _parse_hhmm(value: str) -> time:
    parts = value.strip().split(":", 1)
    if len(parts) != 2:
        raise ValueError(f"时间格式应为 HH:MM: {value!r}")
    hour, minute = int(parts[0]), int(parts[1])
    return time(hour, minute)


def quotes_api_call_allowed(*, at: datetime | None = None) -> bool:
    policy = load_monitor_policy()
    if not policy.quotes_api_call_window_enabled:
        return True
    tz = monitor_timezone(policy)
    moment = at.astimezone(tz) if at is not None else datetime.now(tz)
    start = _parse_hhmm(policy.quotes_api_call_start)
    end = _parse_hhmm(policy.quotes_api_call_end)
    current = moment.time().replace(second=0, microsecond=0)
    end_inclusive = time(end.hour, end.minute, 59)
    return start <= current <= end_inclusive


def quotes_api_call_skip_reason() -> str:
    policy = load_monitor_policy()
    return (
        f"quotes/api 相关用例仅在 {policy.quotes_api_call_start}–{policy.quotes_api_call_end} "
        f"（{policy.quotes_api_call_timezone}）执行，当前时段跳过"
    )
