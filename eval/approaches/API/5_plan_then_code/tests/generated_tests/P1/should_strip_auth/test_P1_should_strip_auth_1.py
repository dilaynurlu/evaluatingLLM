from requests.sessions import Session

def test_should_strip_auth_on_hostname_change():
    """
    Test that authentication headers are stripped when redirecting to a different hostname.
    """
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # When hostname changes, should_strip_auth should return True
    assert session.should_strip_auth(old_url, new_url) is True