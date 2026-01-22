import pytest
from requests.sessions import Session

def test_should_strip_auth_on_different_host():
    """
    Test that Authorization header is stripped when redirecting to a different hostname.
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # Logic: old_parsed.hostname != new_parsed.hostname -> return True
    assert session.should_strip_auth(old_url, new_url) is True