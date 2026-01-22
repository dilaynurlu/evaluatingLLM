from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_1():
    # Same host, no strip
    mixin = SessionRedirectMixin()
    old = "http://example.com/foo"
    new = "http://example.com/bar"
    assert mixin.should_strip_auth(old, new) is False