from requests.sessions import Session

def test_should_strip_auth_default_port():
    s = Session()
    # http:80 is same as http:None
    old = "http://example.com:80/foo"
    new = "http://example.com/bar"
    assert s.should_strip_auth(old, new) is False
    
    # https:443 is same as https:None
    old2 = "https://example.com:443/foo"
    new2 = "https://example.com/bar"
    assert s.should_strip_auth(old2, new2) is False
    
    # http -> https (default ports)
    old3 = "http://example.com:80/foo"
    new3 = "https://example.com:443/bar"
    assert s.should_strip_auth(old3, new3) is False
