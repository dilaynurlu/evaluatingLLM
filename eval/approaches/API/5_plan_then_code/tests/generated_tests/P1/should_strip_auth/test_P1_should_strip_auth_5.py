from requests.sessions import Session

def test_should_strip_auth_on_https_to_http_downgrade():
    """
    Test that auth is stripped when downgrading from https to http,
    even if standard ports are used.
    """
    session = Session()
    old_url = "https://example.com/resource"
    new_url = "http://example.com/resource"
    
    # Downgrade does not match the special case -> return True (changed_scheme is True)
    assert session.should_strip_auth(old_url, new_url) is True