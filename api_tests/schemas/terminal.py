"""终端相关响应 JSON Schema（按实际接口字段调整）。"""

TERMINAL_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "name", "status"],
    "properties": {
        "id": {"type": ["string", "integer"]},
        "name": {"type": "string"},
        "status": {"type": "string"},
        "host": {"type": "string"},
        "last_seen_at": {"type": ["string", "null"]},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
    },
    "additionalProperties": True,
}

TERMINAL_LIST_SCHEMA: dict = {
    "type": "object",
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": TERMINAL_ITEM_SCHEMA,
        },
        "total": {"type": "integer"},
        "page": {"type": "integer"},
        "page_size": {"type": "integer"},
    },
    "additionalProperties": True,
}
