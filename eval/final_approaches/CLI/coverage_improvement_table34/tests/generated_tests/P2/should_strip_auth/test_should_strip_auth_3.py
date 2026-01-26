from requests.sessions import Session

def test_should_strip_auth_downgrade():
    s = Session()
    old_url = "https://example.com/foo"
    new_url = "http://example.com/foo"
    assert s.should_strip_auth(old_url, new_url) is True
