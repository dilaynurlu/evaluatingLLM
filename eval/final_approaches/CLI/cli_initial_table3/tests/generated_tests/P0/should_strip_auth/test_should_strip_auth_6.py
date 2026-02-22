from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_6():
    mixin = SessionRedirectMixin()
    # http://example.com:80 == http://example.com
    result = mixin.should_strip_auth("http://example.com:80", "http://example.com")
    assert result is False
