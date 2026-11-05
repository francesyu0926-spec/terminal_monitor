USER_MARKET_GUIDE_SCHEMA: dict = {
    "type": "object",
    "required": ["is_guide"],
    "properties": {
        "is_guide": {"type": "integer", "enum": [0, 1]},
    },
    "additionalProperties": True,
}

USER_VIEW_DETAIL_SCHEMA: dict = {
    "type": "object",
    "required": ["userId", "nickName", "loginCode", "userStatus"],
    "properties": {
        "userId": {"type": "integer"},
        "nickName": {"type": "string"},
        "loginCode": {"type": "string", "minLength": 1},
        "userStatus": {"type": "integer"},
        "mobile": {"type": ["string", "null"]},
        "realname": {"type": ["string", "null"]},
        "email": {"type": ["string", "null"]},
        "company": {"type": ["string", "null"]},
        "avatarUrl": {"type": ["string", "null"]},
        "isTry": {"type": ["integer", "null"]},
        "deadTime": {"type": ["integer", "null"]},
    },
    "additionalProperties": True,
}
