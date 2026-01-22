from requests.sessions import Session

def test_should_strip_auth_upgrade():
    s = Session()
    old_url = "http://example.com/foo"
    new_url = "https://example.com/foo"
    assert s.should_strip_auth(old_url, new_url) is False
