from requests.sessions import Session

def test_should_strip_auth_http_to_https_upgrade_implicit():
    """
    Test that authentication headers are preserved when upgrading from HTTP to HTTPS 
    using standard implicit ports (80 and 443).
    """
    session = Session()
    old_url = "http://example.com/foo"
    new_url = "https://example.com/bar"
    
    # Special case allows http (implicit 80) -> https (implicit 443) to keep auth
    assert session.should_strip_auth(old_url, new_url) is False