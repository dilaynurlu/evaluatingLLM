import pytest
from requests.sessions import Session

def test_should_strip_auth_http_to_https_implicit():
    """
    Test that Authorization header is preserved (NOT stripped) when upgrading 
    from HTTP to HTTPS on standard ports (implicit).
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "https://example.com/resource"
    
    # This is a special case in requests allowing http -> https upgrade without stripping auth
    assert session.should_strip_auth(old_url, new_url) is False