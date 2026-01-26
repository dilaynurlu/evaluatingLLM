from requests.sessions import Session

def test_should_strip_auth_different_hostname():
    """
    Test that authentication is stripped when redirecting to a different hostname.
    Refined to include:
    1. Subdomain isolation (e.g., api.example.com vs example.com).
    2. Distinct IP addresses.
    """
    session = Session()
    
    # Scenario 1: Different domains
    assert session.should_strip_auth("http://example.com/a", "http://other.com/b") is True
    
    # Scenario 2: Subdomain boundaries (security boundary)
    # Auth should not leak from parent to subdomain or vice versa automatically
    assert session.should_strip_auth("http://example.com/a", "http://api.example.com/b") is True
    assert session.should_strip_auth("http://a.example.com/a", "http://b.example.com/b") is True
    
    # Scenario 3: IP Address mismatch
    assert session.should_strip_auth("http://192.168.1.1/a", "http://192.168.1.2/b") is True