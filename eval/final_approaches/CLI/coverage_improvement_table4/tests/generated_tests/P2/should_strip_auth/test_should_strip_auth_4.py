from requests.sessions import Session

def test_should_strip_auth_port_change():
    s = Session()
    old_url = "http://example.com:8080/foo"
    new_url = "http://example.com:8081/foo"
    assert s.should_strip_auth(old_url, new_url) is True
