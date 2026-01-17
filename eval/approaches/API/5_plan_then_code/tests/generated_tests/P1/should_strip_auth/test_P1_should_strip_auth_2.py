from requests.sessions import Session

def test_should_not_strip_auth_on_same_origin_path_change():
    """
    Test that authentication headers are preserved when redirecting to a different path
    on the same host, scheme, and port (implicit).
    """
    session = Session()
    old_url = "http://example.com/old_path"
    new_url = "http://example.com/new_path"
    
    # Same host, scheme, and implicit port -> return False
    assert session.should_strip_auth(old_url, new_url) is False