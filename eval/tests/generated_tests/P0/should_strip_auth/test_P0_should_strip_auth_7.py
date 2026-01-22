from requests.sessions import Session

def test_should_strip_auth_http_to_https_non_standard():
    """
    Test that authentication headers are stripped when changing scheme from HTTP to HTTPS
    if non-standard ports are used.
    """
    session = Session()
    old_url = "http://example.com:8080/foo"
    new_url = "https://example.com:8443/bar"
    
    # The special case only applies to standard ports (80/443).
    # Here ports change and scheme changes, so it should strip auth.
    assert session.should_strip_auth(old_url, new_url) is True