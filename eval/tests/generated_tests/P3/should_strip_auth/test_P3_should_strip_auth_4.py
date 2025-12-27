from requests.sessions import Session

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that authentication headers are stripped when redirecting from HTTPS to HTTP.
    This is a critical security boundary (downgrade attack prevention).
    """
    session = Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/secure"
    
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is True, "Auth should be stripped when downgrading from HTTPS to HTTP"