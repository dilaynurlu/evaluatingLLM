import requests

def test_should_strip_auth_http_to_https_standard_ports():
    """
    Test that Authorization header is KEPT (not stripped) when upgrading from HTTP to HTTPS
    on standard ports (80/None -> 443/None). This is a special compatibility allowance.
    """
    session = requests.Session()
    old_url = "http://example.com/login"
    new_url = "https://example.com/login"
    
    # Expect False because this is an allowed upgrade path for backward compatibility
    assert session.should_strip_auth(old_url, new_url) is False