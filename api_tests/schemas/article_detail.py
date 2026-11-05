ARTICLE_DETAIL_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "title"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "author": {"type": ["string", "null"]},
        "catalog_id": {"type": ["integer", "null"]},
        "summary": {"type": ["string", "null"]},
        "content": {"type": ["string", "null"]},
        "url": {"type": ["string", "null"]},
        "date_updated": {"type": ["integer", "string", "null"]},
        "emotion_pos": {"type": ["integer", "null"]},
        "companies": {"type": ["array", "null"]},
        "others": {"type": ["array", "null"]},
    },
    "additionalProperties": True,
}
