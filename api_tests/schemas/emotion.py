EMOTION_SOLUTION_VIEW_ITEM_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "solutionId": {"type": ["integer", "null"]},
        "solutionName": {"type": ["string", "null"]},
        "schemeId": {"type": ["integer", "null"]},
        "schemeName": {"type": ["string", "null"]},
        "userId": {"type": ["integer", "null"]},
        "createTime": {"type": ["integer", "null"]},
    },
    "anyOf": [
        {"required": ["solutionId"]},
        {"required": ["schemeId"]},
        {"required": ["id"]},
    ],
    "additionalProperties": True,
}
