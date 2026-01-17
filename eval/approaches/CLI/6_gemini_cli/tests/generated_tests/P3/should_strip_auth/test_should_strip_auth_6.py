from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_default_port_http():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("http://example.com:80", "http://example.com") is False
