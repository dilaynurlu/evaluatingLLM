import pytest
from requests.sessions import Session

def test_should_strip_auth_allow_standard_http_to_https_upgrade():
    """
    Test that Authorization header is preserved (NOT stripped) when redirecting 
    from HTTP to HTTPS using standard ports (80/None -> 443/None) on the same host.
    This is a special case to allow security upgrades.
    """
    session = Session()
    
    # Case: http (implicit port 80) -> https (implicit port 443)
    old_url = "http://example.com/foo"
    new_url = "https://example.com/foo"
    
    # Logic: Special case matches -> return False
    assert session.should_strip_auth(old_url, new_url) is False