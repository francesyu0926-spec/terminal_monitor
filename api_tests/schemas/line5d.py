LINE5D_CHART_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["datetime", "price"],
    "properties": {
        "datetime": {"type": "integer"},
        "price": {"type": ["string", "number"]},
        "volume": {"type": ["string", "number", "null"]},
        "averagePrice": {"type": ["string", "number", "null"]},
        "openPrice": {"type": ["string", "number", "null"]},
        "highPrice": {"type": ["string", "number", "null"]},
        "lowPrice": {"type": ["string", "number", "null"]},
    },
    "additionalProperties": True,
}

LINE5D_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["chartItems", "tradeDates"],
    "properties": {
        "chartItems": {
            "type": "array",
            "minItems": 1,
            "items": LINE5D_CHART_ITEM_SCHEMA,
        },
        "tradeDates": {"type": "array"},
        "systemDatetime": {"type": ["integer", "null"]},
    },
    "additionalProperties": True,
}
