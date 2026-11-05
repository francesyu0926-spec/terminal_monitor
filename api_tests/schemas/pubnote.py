LAWS_TYPE_QUERY_SCHEMA: dict = {
    "type": "array",
    "minItems": 1,
    "items": {"type": "string", "minLength": 1},
}

LAWS_DETAIL_SCHEMA: dict = {
    "type": "object",
    "required": ["seq", "lawsTitle", "lawsContent"],
    "properties": {
        "seq": {"type": "integer"},
        "lawsTitle": {"type": "string"},
        "lawsType": {"type": ["string", "null"]},
        "mechanism": {"type": ["string", "null"]},
        "releaseTime": {"type": ["integer", "null"]},
        "lawsContent": {"type": "string"},
    },
    "additionalProperties": True,
}

LAWS_QUERY_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["seq", "lawsTitle", "lawsType"],
    "properties": {
        "seq": {"type": "integer"},
        "lawsTitle": {"type": "string"},
        "lawsType": {"type": "string"},
        "mechanism": {"type": ["string", "null"]},
        "releaseTime": {"type": ["integer", "null"]},
        "lawsContent": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
