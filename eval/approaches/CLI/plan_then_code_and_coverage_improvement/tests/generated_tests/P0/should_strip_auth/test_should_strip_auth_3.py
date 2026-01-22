from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_3():
    # http -> https upgrade
    mixin = SessionRedirectMixin()
    old = "http://example.com"
    new = "https://example.com"
    assert mixin.should_strip_auth(old, new) is False
