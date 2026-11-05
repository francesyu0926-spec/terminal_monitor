BANNER_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "title", "status"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "imageUrl": {"type": ["string", "null"]},
        "image": {"type": ["string", "null"]},
        "status": {"type": "integer"},
        "orders": {"type": ["integer", "null"]},
        "position": {"type": ["integer", "null"]},
        "category": {"type": ["integer", "null"]},
    },
    "additionalProperties": True,
}
