import requests

def test_should_strip_auth_http_https_upgrade_standard():
    """
    Test that Authorization headers are preserved (NOT stripped) when upgrading 
    from HTTP to HTTPS on standard ports (80/443 or implicit).
    This covers the special backward compatibility case in should_strip_auth.
    """
    session = requests.Session()
    
    # Case: Implicit ports (http=80, https=443 implied)
    old_url = "http://example.com/foo"
    new_url = "https://example.com/bar"
    
    # Logic: Special case allow http->https on standard ports
    assert session.should_strip_auth(old_url, new_url) is False

    # Case: Explicit standard ports
    old_url_explicit = "http://example.com:80/foo"
    new_url_explicit = "https://example.com:443/bar"
    
    assert session.should_strip_auth(old_url_explicit, new_url_explicit) is False