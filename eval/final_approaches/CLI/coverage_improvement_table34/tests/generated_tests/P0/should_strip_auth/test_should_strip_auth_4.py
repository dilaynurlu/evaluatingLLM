from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_4():
    # https -> http downgrade
    mixin = SessionRedirectMixin()
    old = "https://example.com"
    new = "http://example.com"
    assert mixin.should_strip_auth(old, new) is True
