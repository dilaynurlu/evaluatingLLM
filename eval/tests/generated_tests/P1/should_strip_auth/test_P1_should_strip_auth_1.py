import pytest
from requests.sessions import Session

def test_should_strip_auth_on_hostname_mismatch():
    """
    Test that Authorization headers are stripped when the hostname changes
    between the old URL and the new URL.
    """
    session = Session()
    old_url = "http://example.com/data"
    new_url = "http://other-host.com/data"
    
    # Logic: old_parsed.hostname != new_parsed.hostname -> return True
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is True, "Auth should be stripped when hostname changes"