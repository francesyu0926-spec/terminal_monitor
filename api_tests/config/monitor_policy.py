"""非密钥监控策略（`config/monitor_policy.json`，不放在 .env）。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY_PATH = _ROOT / "config" / "monitor_policy.json"


@dataclass(frozen=True)
class MonitorPolicy:
    wework_notify_failure_only_after: str = "2026-11-07 00:00:00"


def load_monitor_policy(path: Path | None = None) -> MonitorPolicy:
    policy_path = path or DEFAULT_POLICY_PATH
    if not policy_path.is_file():
        return MonitorPolicy()
    raw = json.loads(policy_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"monitor_policy 应为 JSON 对象: {policy_path}")
    after = raw.get("wework_notify_failure_only_after", MonitorPolicy.wework_notify_failure_only_after)
    return MonitorPolicy(wework_notify_failure_only_after=str(after or "").strip())
