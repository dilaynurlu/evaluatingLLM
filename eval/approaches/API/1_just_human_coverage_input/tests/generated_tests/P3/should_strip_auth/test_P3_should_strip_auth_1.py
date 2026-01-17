import requests
from requests.sessions import Session

def test_should_strip_auth_different_hostname_variations():
    """
    Test that Authorization header is stripped when redirecting to a different hostname,
    subdomain, or IP representation, while respecting case-insensitivity.
    
    Security requirement: 
    - Credentials must be stripped for cross-origin redirects (including subdomains).
    - Credentials must be preserved for case-insensitive matches of the same host.
    """
    session = Session()
    
    # 1. Distinct domains: MUST Strip
    assert session.should_strip_auth("http://example.com/r", "http://other-site.com/r") is True

    # 2. Subdomain boundaries: MUST Strip (distinct origins)
    assert session.should_strip_auth("http://example.com/r", "http://sub.example.com/r") is True
    assert session.should_strip_auth("http://sub.example.com/r", "http://example.com/r") is True

    # 3. Hostname vs IP literal: MUST Strip (string mismatch implies different context)
    assert session.should_strip_auth("http://localhost/r", "http://127.0.0.1/r") is True

    # 4. Case sensitivity: MUST NOT Strip (DNS is case-insensitive)
    assert session.should_strip_auth("http://example.com/r", "http://EXAMPLE.COM/r") is False