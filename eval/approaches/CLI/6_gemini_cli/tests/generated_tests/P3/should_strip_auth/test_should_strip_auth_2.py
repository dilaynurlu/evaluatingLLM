from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_same_host():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("http://example.com/foo", "http://example.com/bar") is False
