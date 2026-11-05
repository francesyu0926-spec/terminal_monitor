OHLC_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["date", "openPrice", "highPrice", "lowPrice", "closePrice"],
    "properties": {
        "date": {"type": "string"},
        "time": {"type": "string"},
        "openPrice": {"type": "number"},
        "highPrice": {"type": "number"},
        "lowPrice": {"type": "number"},
        "closePrice": {"type": "number"},
        "volume": {"type": "number"},
        "amount": {"type": "number"},
        "preClose": {"type": "number"},
        "adjFactor": {"type": "number"},
        "forwardFactor": {"type": "number"},
        "backwardFactor": {"type": "number"},
    },
    "additionalProperties": True,
}

DAYK_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["OHLCItems"],
    "properties": {
        "OHLCItems": {
            "type": "array",
            "minItems": 1,
            "items": OHLC_ITEM_SCHEMA,
        },
    },
    "additionalProperties": True,
}
