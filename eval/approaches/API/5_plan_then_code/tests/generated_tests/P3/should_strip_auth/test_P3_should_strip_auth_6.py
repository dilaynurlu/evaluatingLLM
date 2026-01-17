import pytest
from requests.sessions import Session

@pytest.mark.parametrize("old_url, new_url", [
    ("http://example.com:8080/resource", "https://example.com:8443/resource"),
    ("http://example.com:80/resource", "https://example.com:8443/resource"),
    ("http://example.com:8080/resource", "https://example.com/resource"),
])
def test_should_strip_auth_non_standard_upgrade(old_url, new_url):
    """
    Test that the HTTP->HTTPS exception does NOT apply if ports are non-standard.
    Auth should be stripped in this case.
    """
    session = Session()
    # The secure upgrade exception is strict about standard ports (80/443).
    assert session.should_strip_auth(old_url, new_url) is True