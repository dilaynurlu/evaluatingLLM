from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_5():
    mixin = SessionRedirectMixin()
    result = mixin.should_strip_auth("http://example.com:8080", "http://example.com:9090")
    assert result is True
