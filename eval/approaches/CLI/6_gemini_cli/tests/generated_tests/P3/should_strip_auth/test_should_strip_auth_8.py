from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_scheme_change():
    mixin = SessionRedirectMixin()
    assert mixin.should_strip_auth("ftp://example.com", "http://example.com") is True
