ES_SEARCH_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "report_title"],
    "properties": {
        "id": {"type": "integer"},
        "report_title": {"type": "string"},
        "report_source": {"type": ["string", "null"]},
        "report_author": {"type": ["string", "null"]},
        "report_type": {"type": ["string", "null"]},
        "report_date": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
