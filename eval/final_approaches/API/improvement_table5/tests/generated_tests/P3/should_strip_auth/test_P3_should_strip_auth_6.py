from requests.sessions import Session

def test_should_strip_auth_same_origin():
    """
    Test that authentication is preserved when redirecting to a URL
    with the same scheme, host, and port.
    Refined to cover:
    1. Case insensitivity (EXAMPLE.COM vs example.com).
    2. URLs containing UserInfo.
    """
    session = Session()
    
    # Scenario 1: Standard same origin
    assert session.should_strip_auth("http://example.com/a", "http://example.com/b") is False
    
    # Scenario 2: Hostname case insensitivity
    # RFC 3986 states hostnames are case-insensitive.
    # Logic: Parsed hostnames should match after normalization.
    assert session.should_strip_auth("http://example.com/a", "http://EXAMPLE.COM/b") is False
    
    # Scenario 3: UserInfo presence
    # The presence of user info in the URL string shouldn't confuse the origin check.
    old_auth = "http://user:pass@example.com/resource"
    new_auth = "http://user:pass@example.com/resource2"
    assert session.should_strip_auth(old_auth, new_auth) is False