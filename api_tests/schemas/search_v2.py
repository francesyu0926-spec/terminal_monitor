SEARCH_V2_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["code", "name", "market"],
    "properties": {
        "market": {"type": "string"},
        "code": {"type": "string"},
        "name": {"type": "string"},
        "pinyin": {"type": ["string", "null"]},
        "type": {"type": ["string", "null"]},
        "HHFlag": {"type": ["string", "null"]},
        "HZFlag": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
