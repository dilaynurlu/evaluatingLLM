from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_https_to_http():
    """
    Test that auth is stripped for https -> http (downgrade).
    """
    mixin = SessionRedirectMixin()
    old_url = "https://example.com/foo"
    new_url = "http://example.com/bar"
    
    assert mixin.should_strip_auth(old_url, new_url) is True
