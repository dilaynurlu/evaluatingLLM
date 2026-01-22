from requests.sessions import Session

def test_should_strip_auth_different_port():
    """
    Test that authentication headers are stripped when redirecting to a different port 
    on the same host (non-default ports).
    """
    session = Session()
    old_url = "http://example.com:8080/api"
    new_url = "http://example.com:9090/api"
    
    # When ports differ and are not equivalent default ports, it should return True
    assert session.should_strip_auth(old_url, new_url) is True