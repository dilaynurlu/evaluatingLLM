from requests.sessions import Session

def test_should_strip_auth_http_to_https_upgrade_standard():
    """
    Test that authentication is preserved when upgrading from HTTP to HTTPS
    on the same host using standard ports.
    """
    session = Session()
    old_url = "http://example.com/dashboard"
    new_url = "https://example.com/dashboard"
    
    # Logic: scheme http->https, standard ports, same host
    # Expected: False (Preserve auth for secure upgrade)
    assert session.should_strip_auth(old_url, new_url) is False