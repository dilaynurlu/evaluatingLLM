from requests.sessions import Session

def test_should_strip_auth_http_to_https_upgrade_case_insensitive():
    """
    Test that authentication headers are preserved when upgrading from HTTP to HTTPS
    even if the hostname casing differs. This ensures the hostname comparison 
    is robust and case-insensitive (e.g., example.com vs EXAMPLE.COM).
    """
    session = Session()
    old_url = "http://example.com/login"
    new_url = "https://EXAMPLE.COM/login"
    
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is False, "Auth should NOT be stripped for case-insensitive HTTP->HTTPS upgrade"