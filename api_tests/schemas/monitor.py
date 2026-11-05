MONITOR_SCHEME_VIEW_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["schemeId", "schemeName", "userId"],
    "properties": {
        "schemeId": {"type": "integer"},
        "schemeName": {"type": "string", "minLength": 1},
        "userId": {"type": "integer"},
        "createTime": {"type": ["integer", "null"]},
        "deleteFlag": {"type": ["boolean", "null"]},
        "hwnTag": {"type": ["integer", "null"]},
        "markets": {"type": ["string", "null"]},
        "regions": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}

MONITOR_SCHEME_VIEW_DETAIL_SCHEMA: dict = {
    "type": "object",
    "required": ["schemeId", "schemeName", "userId", "bonds", "companies", "funds"],
    "properties": {
        "schemeId": {"type": "integer"},
        "schemeName": {"type": "string", "minLength": 1},
        "userId": {"type": "integer"},
        "bonds": {"type": "array"},
        "companies": {"type": "array"},
        "funds": {"type": "array"},
    },
    "additionalProperties": True,
}

MONITOR_GROUP_SEARCH_ITEM_SCHEMA: dict = {
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
    },
    "additionalProperties": True,
}
