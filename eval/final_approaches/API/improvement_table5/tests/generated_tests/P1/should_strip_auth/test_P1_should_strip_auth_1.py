import pytest
from requests.sessions import Session

def test_should_strip_auth_different_hosts():
    """
    Test that Authorization header is stripped when redirecting to a different hostname.
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # When hostnames differ, should_strip_auth must return True to prevent leaking credentials
    assert session.should_strip_auth(old_url, new_url) is True