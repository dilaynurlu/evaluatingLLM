from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_same_url():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("http://example.com", "http://example.com") is False
