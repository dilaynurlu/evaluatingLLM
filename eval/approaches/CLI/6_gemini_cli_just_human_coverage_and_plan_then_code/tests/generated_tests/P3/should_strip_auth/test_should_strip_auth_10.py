from requests.sessions import SessionRedirectMixin

def test_should_strip_auth_custom_to_standard_https():
    mixin = SessionRedirectMixin()
    # 8443 -> 443 (change port)
    assert mixin.should_strip_auth("https://example.com:8443", "https://example.com") is True
