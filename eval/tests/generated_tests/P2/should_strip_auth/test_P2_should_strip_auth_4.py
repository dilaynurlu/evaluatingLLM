import requests

def test_should_strip_auth_on_secure_upgrade_non_standard_ports():
    """
    Test that Authorization headers are stripped when upgrading from HTTP to HTTPS
    if the ports are non-standard. The special exemption only applies to standard ports.
    """
    session = requests.Session()
    old_url = "http://example.com:8080/api"
    new_url = "https://example.com:8443/api"
    
    # Non-standard ports do not match the special case criteria.
    # Scheme changed and port changed -> return True.
    assert session.should_strip_auth(old_url, new_url) is True