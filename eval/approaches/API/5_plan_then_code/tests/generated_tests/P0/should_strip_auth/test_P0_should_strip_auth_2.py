import pytest
from requests import Session

def test_should_strip_auth_http_to_https_standard_ports():
    """
    Test that Authorization headers are NOT stripped when upgrading from HTTP to HTTPS
    on standard ports (special case for backward compatibility/security upgrades).
    """
    session = Session()
    # Case: implicit ports (None -> None) for http -> https
    old_url = "http://example.com/login"
    new_url = "https://example.com/login"
    
    # Expect False because this is a secure upgrade allowed by the special case
    assert session.should_strip_auth(old_url, new_url) is False