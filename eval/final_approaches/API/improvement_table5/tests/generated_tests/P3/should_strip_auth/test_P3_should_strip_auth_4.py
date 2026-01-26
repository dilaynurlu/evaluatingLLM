from requests.sessions import Session

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that authentication is stripped when downgrading scheme.
    Refined to include cross-protocol redirects (HTTP -> FTP).
    """
    session = Session()
    
    # Scenario 1: HTTPS -> HTTP Downgrade
    assert session.should_strip_auth("https://example.com/a", "http://example.com/b") is True
    
    # Scenario 2: HTTP -> FTP (Cross-protocol)
    # Logic: Scheme changed, and it's not the specific http->https upgrade exception.
    assert session.should_strip_auth("http://example.com/a", "ftp://example.com/b") is True