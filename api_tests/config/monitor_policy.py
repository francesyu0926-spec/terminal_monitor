"""非密钥监控策略：只读 `config/monitor_policy.json`（不读 .env 中的同名配置）。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY_PATH = _ROOT / "config" / "monitor_policy.json"


@dataclass(frozen=True)
class MonitorPolicy:
    wework_notify_failure_only_after: str = "2026-11-07 00:00:00"
    quotes_api_call_window_enabled: bool = True
    quotes_api_call_timezone: str = "Asia/Shanghai"
    quotes_api_call_start: str = "09:30"
    quotes_api_call_end: str = "23:39"


def _policy_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "on")
    return bool(value)


def load_monitor_policy(path: Path | None = None) -> MonitorPolicy:
    policy_path = path or DEFAULT_POLICY_PATH
    if not policy_path.is_file():
        return MonitorPolicy()
    raw = json.loads(policy_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"monitor_policy 应为 JSON 对象: {policy_path}")
    return MonitorPolicy(
        wework_notify_failure_only_after=str(
            raw.get("wework_notify_failure_only_after", MonitorPolicy.wework_notify_failure_only_after)
            or ""
        ).strip(),
        quotes_api_call_window_enabled=_policy_bool(
            raw.get("quotes_api_call_window_enabled"),
            MonitorPolicy.quotes_api_call_window_enabled,
        ),
        quotes_api_call_timezone=str(
            raw.get("quotes_api_call_timezone", MonitorPolicy.quotes_api_call_timezone)
        ).strip(),
        quotes_api_call_start=str(
            raw.get("quotes_api_call_start", MonitorPolicy.quotes_api_call_start)
        ).strip(),
        quotes_api_call_end=str(
            raw.get("quotes_api_call_end", MonitorPolicy.quotes_api_call_end)
        ).strip(),
    )


def monitor_timezone(policy: MonitorPolicy | None = None) -> timezone | ZoneInfo:
    """策略里配置的时区（企微起始时刻、行情窗口共用）。"""
    name = (policy or load_monitor_policy()).quotes_api_call_timezone
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        if name in ("Asia/Shanghai", "PRC", "CST-8"):
            return timezone(timedelta(hours=8), name="Asia/Shanghai")
        raise
