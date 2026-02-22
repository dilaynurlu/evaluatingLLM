from requests.sessions import Session

def test_should_strip_auth_same():
    s = Session()
    old = "http://example.com/foo"
    new = "http://example.com/bar"
    assert s.should_strip_auth(old, new) is False
    
    old_https = "https://example.com/foo"
    new_https = "https://example.com/bar"
    assert s.should_strip_auth(old_https, new_https) is False
