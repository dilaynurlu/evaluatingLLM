from requests.sessions import Session

def test_should_strip_auth_scheme_change():
    s = Session()
    old_url = "http://example.com/foo"
    new_url = "ftp://example.com/foo"
    assert s.should_strip_auth(old_url, new_url) is True
