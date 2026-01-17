from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_http_to_https():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("http://example.com", "https://example.com") is False
