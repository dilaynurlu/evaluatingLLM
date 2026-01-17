import pytest
from requests.utils import get_auth_from_url

@pytest.mark.parametrize("url, expected", [
    ("http://user:@example.com", ("user", "")),
    ("http://:password@example.com", ("", "password")),
    ("http://:@example.com", ("", "")),
])
def test_get_auth_from_url_partial_credentials(url, expected):
    """
    Test extraction when only username, only password, or empty placeholders are provided.
    """
    assert get_auth_from_url(url) == expected