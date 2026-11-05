QUOTE_ITEM_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "code": {"type": "string"},
        "name": {"type": "string"},
        "preClosePrice": {"type": ["string", "number", "null"]},
    },
    "additionalProperties": True,
}

QUOTE_ITEMS_LIST_SCHEMA: dict = {
    "type": "object",
    "required": ["quoteItems"],
    "properties": {
        "quoteItems": {
            "type": "array",
            "minItems": 1,
            "items": QUOTE_ITEM_SCHEMA,
        },
    },
    "additionalProperties": True,
}

QUOTE_RESPONSE_SCHEMA = QUOTE_ITEMS_LIST_SCHEMA
