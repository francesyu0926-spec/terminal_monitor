ARTICLE_SHARE_SYSTEM_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "title", "status"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "status": {"type": "integer"},
        "type": {"type": ["integer", "null"]},
        "position": {"type": ["integer", "null"]},
        "articleTable": {"type": ["integer", "null"]},
        "views": {"type": ["integer", "null"]},
        "createTime": {"type": ["integer", "null"]},
        "updateTime": {"type": ["integer", "null"]},
        "companyUrl": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
