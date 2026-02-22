from requests.sessions import Session

def test_should_strip_auth_upgrade():
    s = Session()
    old = "http://example.com/foo"
    new = "https://example.com/bar"
    # This upgrade is allowed, auth preserved.
    assert s.should_strip_auth(old, new) is False
