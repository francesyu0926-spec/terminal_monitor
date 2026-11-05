COMPANY_NOTICE_ITEM_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "infoTitle", "secuCode"],
    "properties": {
        "id": {"type": "integer"},
        "infoTitle": {"type": "string"},
        "secuCode": {"type": "string"},
        "secuAbbr": {"type": ["string", "null"]},
        "type": {"type": ["integer", "null"]},
        "infoPublDate": {"type": ["integer", "null"]},
        "insertTime": {"type": ["integer", "null"]},
    },
    "additionalProperties": True,
}
