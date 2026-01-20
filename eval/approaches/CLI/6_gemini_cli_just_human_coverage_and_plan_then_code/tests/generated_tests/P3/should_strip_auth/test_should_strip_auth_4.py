from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_https_to_http():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("https://example.com", "http://example.com") is True
