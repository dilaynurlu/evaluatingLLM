import pytest
from requests.sessions import Session

@pytest.mark.parametrize("old_url, new_url", [
    ("http://example.com/foo", "http://example.com/bar"),
    ("http://EXAMPLE.COM/foo", "http://example.com/bar"),
    ("http://example.com/foo", "http://EXAMPLE.COM/bar"),
    ("http://exämple.com/foo", "http://exämple.com/bar"),
])
def test_should_strip_auth_origin_normalization(old_url, new_url):
    """
    Test that authentication is preserved when the hostname matches case-insensitively,
    or handles IDN characters correctly, while path/query changes are ignored.
    """
    session = Session()
    # Hostnames are case-insensitive.
    assert session.should_strip_auth(old_url, new_url) is False