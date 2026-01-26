from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_2():
    # Different host
    mixin = SessionRedirectMixin()
    old = "http://example.com"
    new = "http://other.com"
    assert mixin.should_strip_auth(old, new) is True
