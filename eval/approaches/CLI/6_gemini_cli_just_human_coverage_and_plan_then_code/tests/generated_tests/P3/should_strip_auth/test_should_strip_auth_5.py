from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_port_change():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("http://example.com:8080", "http://example.com:9090") is True
