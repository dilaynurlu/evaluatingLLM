from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_2():
    # Different host, strip
    mixin = SessionRedirectMixin()
    old = "http://example.com/foo"
    new = "http://other.com/bar"
    assert mixin.should_strip_auth(old, new) is True