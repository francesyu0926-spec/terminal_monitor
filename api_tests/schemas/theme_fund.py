THEME_FUND_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["fundCode", "fundName"],
    "properties": {
        "fundCode": {"type": "string"},
        "fundName": {"type": "string"},
        "endDate": {"type": ["string", "null"]},
        "type": {"type": ["string", "null"]},
        "unitNav": {"type": ["number", "null"]},
        "rate": {"type": ["number", "null"]},
        "navgrtd": {"type": ["number", "null"]},
    },
    "additionalProperties": True,
}
