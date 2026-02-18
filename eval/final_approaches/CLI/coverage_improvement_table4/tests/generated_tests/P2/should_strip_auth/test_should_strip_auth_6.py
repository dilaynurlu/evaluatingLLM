from requests.sessions import Session

def test_should_strip_auth_upgrade_explicit():
    s = Session()
    old_url = "http://example.com:80/foo"
    new_url = "https://example.com:443/foo"
    assert s.should_strip_auth(old_url, new_url) is False
