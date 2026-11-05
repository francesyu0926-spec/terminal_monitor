"""终端 CRUD 脚手架用例：依赖 {API_PREFIX}/terminals，生产 sfccn 未部署，不参与 smoke。"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.schemas.terminal import TERMINAL_ITEM_SCHEMA, TERMINAL_LIST_SCHEMA
from api_tests.services.terminal_api import TerminalApi


@pytest.mark.regression
@pytest.mark.terminal
def test_list_terminals(terminal_api: TerminalApi) -> None:
    resp = terminal_api.list(page=1, page_size=10)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert_json_schema(body, TERMINAL_LIST_SCHEMA)


@pytest.mark.regression
@pytest.mark.terminal
def test_get_terminal_by_id(terminal_api: TerminalApi, created_terminal: str) -> None:
    resp = terminal_api.get(created_terminal)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    item = body.get("data", body)
    assert_json_schema(item, TERMINAL_ITEM_SCHEMA)
    assert str(item.get("id")) == created_terminal


@pytest.mark.regression
@pytest.mark.terminal
def test_update_terminal(terminal_api: TerminalApi, created_terminal: str) -> None:
    payload = {"status": "offline", "name": "updated-by-automation"}
    resp = terminal_api.update(created_terminal, payload)
    assert resp.status_code in (200, 204), resp.text

    get_resp = terminal_api.get(created_terminal)
    assert get_resp.status_code == 200
    item = get_resp.json().get("data", get_resp.json())
    assert item.get("status") == "offline"


@pytest.mark.regression
@pytest.mark.terminal
def test_delete_terminal(terminal_api: TerminalApi, terminal_create_payload: dict) -> None:
    create_resp = terminal_api.create(terminal_create_payload)
    assert create_resp.status_code in (200, 201), create_resp.text
    body = create_resp.json()
    terminal_id = body.get("id") or body.get("data", {}).get("id")
    assert terminal_id is not None

    del_resp = terminal_api.delete(terminal_id)
    assert del_resp.status_code in (200, 204, 404)

    get_resp = terminal_api.get(terminal_id)
    assert get_resp.status_code == 404
