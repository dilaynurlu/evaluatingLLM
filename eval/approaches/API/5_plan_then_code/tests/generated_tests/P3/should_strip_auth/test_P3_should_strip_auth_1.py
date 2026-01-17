import pytest
from requests.sessions import Session

@pytest.mark.parametrize("old_url, new_url", [
    ("http://example.com/resource", "http://other-domain.com/resource"),
    ("http://example.com/resource", "http://sub.example.com/resource"),
    ("http://api.example.com/resource", "http://web.example.com/resource"),
    ("http://localhost/resource", "http://127.0.0.1/resource"),
    ("http://[::1]/resource", "http://[::2]/resource"),
    ("http://exämple.com/resource", "http://other.com/resource"),
])
def test_should_strip_auth_hostname_mismatches(old_url, new_url):
    """
    Test that authentication headers are stripped when redirecting to a different hostname,
    IP address, or subdomain.
    """
    session = Session()
    # When hostnames, subdomains, or IP literals differ, auth should be stripped.
    assert session.should_strip_auth(old_url, new_url) is True