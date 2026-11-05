YQT_SSO_TOKEN_SCHEMA: dict = {
    "type": "object",
    "required": [
        "timeStamp",
        "systemId",
        "clientUserName",
        "channel",
        "directUrl",
        "encryptCode",
        "accessToken",
    ],
    "properties": {
        "timeStamp": {"type": "integer"},
        "systemId": {"type": "string", "minLength": 1},
        "clientUserName": {"type": "string", "minLength": 1},
        "channel": {"type": "string", "minLength": 1},
        "directUrl": {"type": "string", "minLength": 1},
        "encryptCode": {"type": "string", "minLength": 1},
        "accessToken": {"type": "string", "minLength": 1},
    },
    "additionalProperties": True,
}
