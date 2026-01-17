import pytest
from requests.sessions import Session

@pytest.mark.parametrize("old_url, new_url", [
    ("http://example.com:80/resource", "http://example.com/resource"),
    ("http://example.com/resource", "http://example.com:80/resource"),
    ("https://example.com:443/resource", "https://example.com/resource"),
    ("https://example.com/resource", "https://example.com:443/resource"),
])
def test_should_strip_auth_default_port_normalization(old_url, new_url):
    """
    Test that authentication is preserved when one URL uses an explicit default port
    (80 for HTTP, 443 for HTTPS) and the other uses the implicit default port.
    """
    session = Session()
    # These pairs are effectively the same origin.
    assert session.should_strip_auth(old_url, new_url) is False