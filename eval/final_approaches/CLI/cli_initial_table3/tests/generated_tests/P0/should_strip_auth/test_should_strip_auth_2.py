from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_2():
    mixin = SessionRedirectMixin()
    result = mixin.should_strip_auth("http://example.com", "http://evil.com")
    assert result is True
