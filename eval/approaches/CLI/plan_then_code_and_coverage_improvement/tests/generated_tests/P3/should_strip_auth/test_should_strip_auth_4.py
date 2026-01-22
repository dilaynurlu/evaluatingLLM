from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_4():
    # Port change, strip
    mixin = SessionRedirectMixin()
    old = "http://example.com:8080/foo"
    new = "http://example.com:9090/bar"
    assert mixin.should_strip_auth(old, new) is True
