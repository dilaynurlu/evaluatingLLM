import pytest
from requests.sessions import Session

def test_should_strip_auth_hostname_mismatch():
    """
    Test that authentication is stripped when redirecting to a different hostname.
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-host.com/resource"
    
    # Different hostname -> should strip auth (return True)
    assert session.should_strip_auth(old_url, new_url) is True