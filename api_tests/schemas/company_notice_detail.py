COMPANY_NOTICE_DETAIL_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "infoTitle", "content"],
    "properties": {
        "id": {"type": "integer"},
        "infoTitle": {"type": "string"},
        "content": {"type": "string"},
        "announcementLink": {"type": ["string", "null"]},
        "insertTime": {"type": ["integer", "null"]},
    },
    "additionalProperties": True,
}
