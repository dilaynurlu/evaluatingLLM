from requests.sessions import Session

def test_should_strip_auth_on_explicit_port_change():
    """
    Test that auth is stripped when changing between two different non-standard ports
    on the same host and scheme.
    """
    session = Session()
    old_url = "http://example.com:8080/resource"
    new_url = "http://example.com:9090/resource"
    
    # Different ports -> return True
    assert session.should_strip_auth(old_url, new_url) is True