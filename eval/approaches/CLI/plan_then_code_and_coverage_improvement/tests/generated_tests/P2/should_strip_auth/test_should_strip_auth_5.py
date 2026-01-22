from requests.sessions import Session

def test_should_strip_auth_default_ports():
    s = Session()
    # http:80 -> http (implicit 80)
    old_url = "http://example.com:80/foo"
    new_url = "http://example.com/foo"
    assert s.should_strip_auth(old_url, new_url) is False
