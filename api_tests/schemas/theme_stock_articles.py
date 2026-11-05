THEME_STOCK_ARTICLE_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["articleId", "title"],
    "properties": {
        "articleId": {"type": "integer"},
        "title": {"type": "string"},
        "author": {"type": ["string", "null"]},
        "content": {"type": ["string", "null"]},
        "publishTime": {"type": ["integer", "null"]},
        "type": {"type": ["integer", "null"]},
    },
    "additionalProperties": True,
}
