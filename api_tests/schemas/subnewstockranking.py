SUBNEW_QUOTE_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["code", "name"],
    "properties": {
        "code": {"type": "string"},
        "name": {"type": "string"},
        "IPOPrice": {"type": ["string", "number", "null"]},
        "lastPrice": {"type": ["string", "number", "null"]},
        "IPODate": {"type": "string"},
        "changeRate": {"type": ["string", "number", "null"]},
    },
    "additionalProperties": True,
}

SUBNEWSTOCKRANKING_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["subnewQuoteItems"],
    "properties": {
        "subnewQuoteItems": {
            "type": "array",
            "minItems": 1,
            "items": SUBNEW_QUOTE_ITEM_SCHEMA,
        },
    },
    "additionalProperties": True,
}
