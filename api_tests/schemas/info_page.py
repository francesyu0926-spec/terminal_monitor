INFO_PAGE_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "title"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "author": {"type": ["string", "null"]},
        "description": {"type": ["string", "null"]},
        "pressdate": {"type": ["integer", "null"]},
        "type": {"type": ["integer", "null"]},
        "url": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
