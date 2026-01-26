from requests.sessions import Session

def test_should_strip_auth_https_downgrade():
    """
    Test that authentication headers are stripped when downgrading from HTTPS to HTTP.
    """
    session = Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # HTTPS -> HTTP is a scheme change that should strip auth (returns True)
    assert session.should_strip_auth(old_url, new_url) is True