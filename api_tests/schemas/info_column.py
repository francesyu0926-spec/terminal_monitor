INFO_COLUMN_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["positionName", "positionType"],
    "properties": {
        "positionName": {"type": "string"},
        "positionType": {"type": "integer"},
        "deprecated": {"type": "integer"},
        "ranking": {"type": "integer"},
    },
    "additionalProperties": True,
}
