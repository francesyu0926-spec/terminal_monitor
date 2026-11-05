ARTICLE_RECENT_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["articleId", "title", "publishTime"],
    "properties": {
        "articleId": {"type": "integer"},
        "title": {"type": "string"},
        "author": {"type": ["string", "null"]},
        "content": {"type": ["string", "null"]},
        "publishTime": {"type": "integer"},
        "type": {"type": "integer"},
        "needLogin": {"type": "boolean"},
        "picUrl": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
