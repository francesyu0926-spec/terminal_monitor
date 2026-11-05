MEETING_INVEST_INDUSTRY_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "id": {"type": ["integer", "string", "null"]},
        "name": {"type": ["string", "null"]},
        "industryName": {"type": ["string", "null"]},
        "code": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
