EMOTION_POINT_SCHEMA: dict = {
    "type": "object",
    "required": ["desc", "ranker", "value"],
    "properties": {
        "desc": {"type": "string"},
        "ranker": {"type": "integer"},
        "value": {"type": "number"},
    },
    "additionalProperties": True,
}

INDEX_EMOTION_DATA_SCHEMA: dict = {
    "type": "object",
    "required": ["today", "yesterday", "weekAgo", "monthAgo", "yearAgo", "updateDate"],
    "properties": {
        "today": EMOTION_POINT_SCHEMA,
        "yesterday": EMOTION_POINT_SCHEMA,
        "weekAgo": EMOTION_POINT_SCHEMA,
        "monthAgo": EMOTION_POINT_SCHEMA,
        "yearAgo": EMOTION_POINT_SCHEMA,
        "updateDate": {"type": "string"},
    },
    "additionalProperties": True,
}
