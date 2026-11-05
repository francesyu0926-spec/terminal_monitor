INDEX_TREND_POINT_SCHEMA: dict = {
    "type": "object",
    "required": ["date", "value"],
    "properties": {
        "date": {"type": "string"},
        "value": {"type": "number"},
    },
    "additionalProperties": True,
}

INDEX_TREND_DATA_SCHEMA: dict = {
    "type": "object",
    "required": ["scope", "trend", "updateDate"],
    "properties": {
        "scope": {"type": "string"},
        "updateDate": {"type": "string"},
        "trend": {
            "type": "array",
            "minItems": 1,
            "items": INDEX_TREND_POINT_SCHEMA,
        },
    },
    "additionalProperties": True,
}
