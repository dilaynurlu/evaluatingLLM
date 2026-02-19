import pytest
from requests.sessions import Session

def test_should_strip_auth_different_hosts():
    """
    Test that Authorization header is stripped when redirecting to a different hostname.
    Matches branch: if old_parsed.hostname != new_parsed.hostname: return True
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # Different hosts -> should strip auth
    assert session.should_strip_auth(old_url, new_url) is True