ARTICLE_FLASH_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["articleId"],
    "properties": {
        "articleId": {"type": "integer"},
        "author": {"type": ["string", "null"]},
        "content": {"type": ["string", "null"]},
        "title": {"type": ["string", "null"]},
        "collectFlag": {"type": "boolean"},
    },
    "additionalProperties": True,
}
