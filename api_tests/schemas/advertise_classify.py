ADVERTISE_CLASSIFY_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "name"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
    },
    "additionalProperties": True,
}
