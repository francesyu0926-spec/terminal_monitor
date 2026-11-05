USER_STOCK_GROUP_NODE_SCHEMA: dict = {
    "type": "object",
    "required": ["gid", "gnm", "stks"],
    "properties": {
        "gid": {"type": "integer"},
        "gnm": {"type": "string"},
        "gorder": {"type": ["integer", "null"]},
        "isSuper": {"type": "boolean"},
        "isTheme": {"type": "boolean"},
        "stks": {"type": "array"},
    },
    "additionalProperties": True,
}

GROUP_WITH_STOCKS_TREE_DATA_SCHEMA: dict = {
    "type": "object",
    "required": ["ver", "tree"],
    "properties": {
        "ver": {"type": "string"},
        "tree": {
            "type": "array",
            "minItems": 1,
            "items": USER_STOCK_GROUP_NODE_SCHEMA,
        },
    },
    "additionalProperties": True,
}
