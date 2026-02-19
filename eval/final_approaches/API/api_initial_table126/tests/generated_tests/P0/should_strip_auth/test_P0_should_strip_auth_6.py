from requests.sessions import Session

def test_should_strip_auth_http_to_https_upgrade_explicit():
    """
    Test that authentication headers are preserved when upgrading from HTTP to HTTPS 
    using explicit standard ports.
    """
    session = Session()
    old_url = "http://example.com:80/foo"
    new_url = "https://example.com:443/bar"
    
    # Special case allows http:80 -> https:443 to keep auth
    assert session.should_strip_auth(old_url, new_url) is False