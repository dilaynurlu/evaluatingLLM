import pytest
from requests.sessions import Session

def test_should_strip_auth_allows_http_to_https_upgrade_standard_ports():
    """
    Test that Authorization headers are PRESERVED (not stripped) when 
    redirecting from HTTP to HTTPS on standard ports (80/None -> 443/None).
    This is a special case in the logic to allow secure upgrades.
    """
    session = Session()
    # Implicit ports: http=80, https=443
    old_url = "http://example.com/login"
    new_url = "https://example.com/login"
    
    # Logic: 
    # schemes: http -> https
    # ports: (80/None) -> (443/None)
    # Matches special exception case -> return False
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is False, "Auth should be preserved when upgrading http -> https on standard ports"