from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_1():
    mixin = SessionRedirectMixin()
    # Same host, same scheme, same port
    result = mixin.should_strip_auth("http://example.com/foo", "http://example.com/bar")
    assert result is False
