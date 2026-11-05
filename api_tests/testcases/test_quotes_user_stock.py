"""自选：/terminal/quotes/user-stock/*"""

import pytest

from api_tests.core.assertions import assert_json_schema
from api_tests.core.response import assert_group_with_stocks_tree_success, parse_json_response
from api_tests.schemas.user_stock_group import GROUP_WITH_STOCKS_TREE_DATA_SCHEMA
from api_tests.services.user_stock_api import UserStockApi


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.quote
def test_group_with_stocks_tree(user_stock_api: UserStockApi) -> None:
    resp = user_stock_api.group_with_stocks_tree()
    body = assert_group_with_stocks_tree_success(parse_json_response(resp))
    assert_json_schema(body["data"], GROUP_WITH_STOCKS_TREE_DATA_SCHEMA)
