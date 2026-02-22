from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_3():
    mixin = SessionRedirectMixin()
    # http -> https on default ports allowed
    result = mixin.should_strip_auth("http://example.com", "https://example.com")
    assert result is False
