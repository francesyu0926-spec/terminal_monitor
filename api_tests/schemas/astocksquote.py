ASTOCKSQUOTE_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["status", "message", "list"],
    "properties": {
        "status": {"type": "integer"},
        "message": {"type": "string"},
        "list": {"type": "array", "items": {"type": "number"}},
        "tTime": {"type": "string"},
        "tUp": {"type": "integer"},
        "tDown": {"type": "integer"},
        "tEqual": {"type": "integer"},
        "tLimitDown": {"type": "integer"},
        "tLimitUp": {"type": "integer"},
    },
    "additionalProperties": True,
}
