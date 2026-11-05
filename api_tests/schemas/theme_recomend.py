THEME_STOCK_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["stocks_code", "stocks_name"],
    "properties": {
        "stocks_code": {"type": "string"},
        "stocks_name": {"type": "string"},
        "theme_id": {"type": "integer"},
        "reason": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}

THEME_RECOMEND_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["theme_id", "theme_name", "themeStocksVOS"],
    "properties": {
        "id": {"type": "integer"},
        "theme_id": {"type": "integer"},
        "theme_name": {"type": "string"},
        "theme_describe": {"type": ["string", "null"]},
        "reason": {"type": ["string", "null"]},
        "themeStocksVOS": {
            "type": "array",
            "minItems": 1,
            "items": THEME_STOCK_ITEM_SCHEMA,
        },
    },
    "additionalProperties": True,
}
