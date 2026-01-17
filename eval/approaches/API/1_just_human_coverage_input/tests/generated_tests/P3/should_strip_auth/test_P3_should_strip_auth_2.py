import requests
from requests.sessions import Session

def test_should_strip_auth_http_to_https_upgrade_standard_ports():
    """
    Test that Authorization header is preserved when upgrading from HTTP to HTTPS 
    on standard ports, including handling of case-insensitive hostnames during upgrade.
    """
    session = Session()
    
    # Standard upgrade: http (80) -> https (443)
    # This is the primary exemption allowing secure upgrades.
    assert session.should_strip_auth("http://example.com/login", "https://example.com/login") is False
    
    # Upgrade with case variation in hostname
    # Should still recognize as same host and allow upgrade.
    assert session.should_strip_auth("http://example.com/login", "https://EXAMPLE.COM/login") is False