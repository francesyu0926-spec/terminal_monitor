NEW_SHARE_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["APPLYCODE", "SECUABBR", "TRADINGCODE"],
    "properties": {
        "APPLYCODE": {"type": "string"},
        "SECUABBR": {"type": "string"},
        "TRADINGCODE": {"type": "string"},
        "ISSUEPRICE": {"type": "string"},
        "LISTINGDATE": {"type": "string"},
        "ISSBGNDT": {"type": "string"},
    },
    "additionalProperties": True,
}

NEWSHARESCAL_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["status", "message", "data"],
    "properties": {
        "status": {"type": "integer"},
        "message": {"type": "string"},
        "data": {
            "type": "object",
            "required": ["wsslist"],
            "properties": {
                "wsslist": {
                    "type": "array",
                    "items": NEW_SHARE_ITEM_SCHEMA,
                },
            },
            "additionalProperties": True,
        },
    },
    "additionalProperties": True,
}
