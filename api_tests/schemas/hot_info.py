HOT_INFO_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "title"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
    },
    "additionalProperties": True,
}

HOT_INFO_DATA_SCHEMA: dict = {
    "type": "object",
    "required": ["hotInfo"],
    "properties": {
        "hotInfo": {
            "type": "array",
            "minItems": 1,
            "items": HOT_INFO_ITEM_SCHEMA,
        },
    },
    "additionalProperties": True,
}
