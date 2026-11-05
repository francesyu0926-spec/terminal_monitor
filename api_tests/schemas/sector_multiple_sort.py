SECTOR_RANK_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["code", "name"],
    "properties": {
        "code": {"type": "string"},
        "name": {"type": "string"},
        "amount": {"type": ["number", "string", "null"]},
        "turnoverRate": {"type": ["number", "string", "null"]},
        "threeMinRise": {"type": ["number", "string", "null"]},
        "lastPrice": {"type": ["number", "string", "null"]},
        "preClosePrice": {"type": ["number", "string", "null"]},
        "fiveMinRise": {"type": ["number", "string", "null"]},
    },
    "additionalProperties": True,
}

SECTOR_MULTIPLE_SORT_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "minProperties": 1,
    "additionalProperties": {
        "type": "array",
        "minItems": 1,
        "items": SECTOR_RANK_ITEM_SCHEMA,
    },
}
