from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_3():
    # Upgrade http -> https (standard ports), no strip
    mixin = SessionRedirectMixin()
    old = "http://example.com/foo"
    new = "https://example.com/bar"
    assert mixin.should_strip_auth(old, new) is False
