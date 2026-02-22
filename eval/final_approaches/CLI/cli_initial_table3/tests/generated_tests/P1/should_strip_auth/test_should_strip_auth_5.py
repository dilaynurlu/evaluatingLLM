from requests.sessions import Session

def test_should_strip_auth_port_change():
    s = Session()
    old = "http://example.com:8080/foo"
    new = "http://example.com:8081/bar"
    # Different port, auth stripped.
    assert s.should_strip_auth(old, new) is True
