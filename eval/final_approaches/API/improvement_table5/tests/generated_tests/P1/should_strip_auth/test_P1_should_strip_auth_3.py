import pytest
from requests.sessions import Session

def test_should_strip_auth_http_to_https_explicit():
    """
    Test that Authorization header is preserved when upgrading from HTTP to HTTPS 
    using explicit standard ports (80 -> 443).
    """
    session = Session()
    old_url = "http://example.com:80/resource"
    new_url = "https://example.com:443/resource"
    
    # Should verify the explicit port check in the special upgrade logic
    assert session.should_strip_auth(old_url, new_url) is False