PARAM_ADDR_NODE_SCHEMA: dict = {
    "type": "object",
    "required": ["code", "zhsname"],
    "properties": {
        "code": {"type": "string", "minLength": 1},
        "zhsname": {"type": "string", "minLength": 1},
        "childAddr": {
            "type": ["array", "null"],
            "items": {"$ref": "#"},
        },
    },
    "additionalProperties": True,
}
