import requests

def test_should_strip_auth_http_to_https_non_standard_ports():
    """
    Test that Authorization header is stripped when upgrading from HTTP to HTTPS
    if non-standard ports are used. The special allowance only applies to standard ports.
    """
    session = requests.Session()
    old_url = "http://example.com:8080/foo"
    new_url = "https://example.com:8443/foo"
    
    # Expect True because the special case check (http/80 -> https/443) fails on ports
    assert session.should_strip_auth(old_url, new_url) is True