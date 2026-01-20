from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_default_port_https():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("https://example.com:443", "https://example.com") is False
