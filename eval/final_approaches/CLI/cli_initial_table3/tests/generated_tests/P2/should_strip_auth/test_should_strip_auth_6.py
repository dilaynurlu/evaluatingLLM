from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_default_port():
    """
    Test that auth is not stripped for default port change (e.g. 80 -> None).
    """
    mixin = SessionRedirectMixin()
    old_url = "http://example.com:80/foo"
    new_url = "http://example.com/bar"
    
    assert mixin.should_strip_auth(old_url, new_url) is False
    assert mixin.should_strip_auth(new_url, old_url) is False
