import pytest
from requests.sessions import Session

def test_should_strip_auth_same_scheme_default_port():
    """
    Test that Authorization header is preserved when redirecting between an implicit 
    default port and an explicit default port on the same scheme (e.g., http -> http:80).
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://example.com:80/resource"
    
    # These are functionally the same origin, so auth should NOT be stripped
    assert session.should_strip_auth(old_url, new_url) is False