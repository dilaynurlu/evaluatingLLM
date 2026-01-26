from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_1():
    # Same host
    mixin = SessionRedirectMixin()
    old = "http://example.com/a"
    new = "http://example.com/b"
    assert mixin.should_strip_auth(old, new) is False
