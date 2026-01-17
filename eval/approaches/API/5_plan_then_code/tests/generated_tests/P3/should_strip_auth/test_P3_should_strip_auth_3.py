import pytest
from requests.sessions import Session

@pytest.mark.parametrize("old_url, new_url", [
    ("https://example.com/resource", "http://example.com/resource"),
    ("https://example.com:443/resource", "http://example.com:80/resource"),
    ("http://example.com/resource", "ftp://example.com/resource"),
    ("https://example.com/resource", "file:///etc/passwd"),
])
def test_should_strip_auth_scheme_downgrades_and_switches(old_url, new_url):
    """
    Test that authentication headers are stripped when downgrading from HTTPS to HTTP,
    or switching to non-HTTP schemes (ftp, file), as this exposes credentials.
    """
    session = Session()
    # Any scheme change that isn't http->https is considered unsafe or cross-protocol.
    assert session.should_strip_auth(old_url, new_url) is True