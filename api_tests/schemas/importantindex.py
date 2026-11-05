DESK_INDEX_DATA_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["status", "message", "data"],
    "properties": {
        "status": {"type": "integer"},
        "message": {"type": "string"},
        "data": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {"type": "string"},
        },
    },
    "additionalProperties": True,
}

IMPORTANTINDEX_RESPONSE_SCHEMA = DESK_INDEX_DATA_RESPONSE_SCHEMA
PROFINMAININDEX_RESPONSE_SCHEMA = DESK_INDEX_DATA_RESPONSE_SCHEMA
PROINCSTATEMENTNEW_RESPONSE_SCHEMA = DESK_INDEX_DATA_RESPONSE_SCHEMA
PROBALSHEETNEW_RESPONSE_SCHEMA = DESK_INDEX_DATA_RESPONSE_SCHEMA
PROCSTATEMENTNEW_RESPONSE_SCHEMA = DESK_INDEX_DATA_RESPONSE_SCHEMA
