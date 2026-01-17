from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_cross_host():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("http://example.com", "http://other.com") is True
