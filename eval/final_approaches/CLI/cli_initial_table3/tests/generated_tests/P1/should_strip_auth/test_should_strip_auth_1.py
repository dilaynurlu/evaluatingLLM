from requests.sessions import Session

def test_should_strip_auth_diff_host():
    s = Session()
    old = "http://example.com/foo"
    new = "http://other.com/foo"
    assert s.should_strip_auth(old, new) is True
