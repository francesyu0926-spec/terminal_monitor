from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator


def assert_json_schema(instance: Any, schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
    if errors:
        messages = "; ".join(f"{list(e.path)}: {e.message}" for e in errors[:5])
        raise AssertionError(f"JSON Schema 校验失败: {messages}")
