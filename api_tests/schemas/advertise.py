ADVERTISE_LIST_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": ["string", "null"]},
        "name": {"type": ["string", "null"]},
        "classifyId": {"type": ["integer", "null"]},
        "status": {"type": ["integer", "null"]},
        "url": {"type": ["string", "null"]},
        "imageUrl": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
