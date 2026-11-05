MONGO_VIEW_THEME_NODE_SCHEMA: dict = {
    "type": "object",
    "required": ["id", "node_cap", "node_code"],
    "properties": {
        "id": {"type": "integer"},
        "p_node_code": {"type": ["integer", "null"]},
        "node_code": {"type": "integer"},
        "node_typ": {"type": ["integer", "null"]},
        "node_cap": {"type": "string", "minLength": 1},
        "obj_vw_eng_name": {"type": ["string", "null"]},
        "sn": {"type": ["integer", "null"]},
        "is_vis": {"type": ["string", "null"]},
        "node_url": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}

MONGO_QUERY_ROW_SCHEMA: dict = {
    "type": "object",
    "required": ["SYMBOL", "SESNAME"],
    "properties": {
        "SYMBOL": {"type": "string", "minLength": 1},
        "SESNAME": {"type": "string", "minLength": 1},
        "TOTALSHARE": {"type": ["number", "null"]},
        "CIRCSKAMT": {"type": ["number", "null"]},
        "ENDDATE": {"type": ["integer", "null"]},
    },
    "additionalProperties": True,
}

MONGO_OBJECT_VIEW_CONFIG_SCHEMA: dict = {
    "type": "object",
    "required": ["obj_vw_id", "obj_prop_cap", "obj_prop_name"],
    "properties": {
        "id": {"type": ["integer", "null"]},
        "obj_vw_id": {"type": "integer"},
        "obj_prop_cap": {"type": "string", "minLength": 1},
        "obj_prop_name": {"type": "string", "minLength": 1},
        "obj_prop_typ": {"type": ["string", "null"]},
        "vw_sts": {"type": ["string", "null"]},
    },
    "additionalProperties": True,
}
