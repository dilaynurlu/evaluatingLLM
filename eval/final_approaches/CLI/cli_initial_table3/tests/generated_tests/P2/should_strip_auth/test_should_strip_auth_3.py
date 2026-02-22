from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_http_to_https():
    """
    Test that auth is not stripped for http -> https (upgrade).
    """
    mixin = SessionRedirectMixin()
    old_url = "http://example.com/foo"
    new_url = "https://example.com/bar"
    
    assert mixin.should_strip_auth(old_url, new_url) is False
