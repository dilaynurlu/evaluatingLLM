from requests.sessions import Session

def test_should_strip_auth_same_host_same_port():
    """
    Test that authentication headers are preserved when redirecting to the same host, 
    scheme, and port.
    """
    session = Session()
    old_url = "http://example.com/page1"
    new_url = "http://example.com/page2"
    
    # When host, scheme, and port are identical, it should return False
    assert session.should_strip_auth(old_url, new_url) is False