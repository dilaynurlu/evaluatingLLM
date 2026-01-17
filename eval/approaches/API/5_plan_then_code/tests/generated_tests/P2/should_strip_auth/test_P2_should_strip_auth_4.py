import requests

def test_should_strip_auth_port_normalization():
    """
    Test that Authorization headers are preserved when switching between 
    explicit default ports and implicit default ports on the same scheme.
    """
    session = requests.Session()
    
    # Case: HTTP explicit 80 -> HTTP implicit
    old_url = "http://example.com:80/resource"
    new_url = "http://example.com/resource"
    
    # Logic: Ports appear different (80 vs None), but are functionally equivalent defaults.
    # The function handles this via DEFAULT_PORTS check.
    assert session.should_strip_auth(old_url, new_url) is False

    # Case: HTTPS implicit -> HTTPS explicit 443
    old_url_secure = "https://example.com/resource"
    new_url_secure = "https://example.com:443/resource"
    
    assert session.should_strip_auth(old_url_secure, new_url_secure) is False