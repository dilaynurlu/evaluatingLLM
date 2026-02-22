from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_4():
    mixin = SessionRedirectMixin()
    # https -> http should strip auth (unsafe downgrade)
    result = mixin.should_strip_auth("https://example.com", "http://example.com")
    assert result is True
