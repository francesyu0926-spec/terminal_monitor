OVERSEAS_REPORT_RECORD_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "title"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string", "minLength": 1},
        "reportType": {"type": ["string", "null"]},
        "industry": {"type": ["string", "null"]},
        "securities": {"type": ["string", "null"]},
        "stockCode": {"type": ["string", "null"]},
        "stockName": {"type": ["string", "null"]},
        "page": {"type": ["integer", "null"]},
        "reDate": {"type": ["string", "null"]},
        "author": {"type": ["string", "null"]},
        "lang": {"type": ["string", "null"]},
        "companycode": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
