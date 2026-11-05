ORGANIZATION_REPORT_DETAIL_SCHEMA: dict = {
    "type": "object",
    "required": ["pid", "title", "contentType"],
    "properties": {
        "pid": {"type": "integer"},
        "id": {"type": ["integer", "null"]},
        "title": {"type": "string"},
        "author": {"type": ["string", "null"]},
        "content": {"type": ["string", "null"]},
        "contentType": {"type": "string"},
        "pubDate": {"type": ["integer", "string", "null"]},
        "sourceName": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}

CONTENT_TYPE_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["contentType"],
    "properties": {
        "contentType": {"type": "string"},
    },
    "additionalProperties": True,
}
