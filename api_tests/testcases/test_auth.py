import pytest

from api_tests.auth.login import login_with_password
from api_tests.auth.token_provider import TokenProvider


@pytest.mark.smoke
@pytest.mark.auth
def test_login_returns_jwt_token() -> None:
    token = login_with_password()
    assert isinstance(token, str)
    assert token.count(".") >= 2


@pytest.mark.smoke
@pytest.mark.auth
def test_token_provider_reuses_cached_token(token_provider: TokenProvider) -> None:
    first = token_provider.get_token()
    second = token_provider.get_token()
    assert first == second
