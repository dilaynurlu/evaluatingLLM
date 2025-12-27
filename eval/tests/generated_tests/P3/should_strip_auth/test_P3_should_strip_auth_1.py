from requests.sessions import Session

def test_should_strip_auth_subdomain_change():
    """
    Test that authentication headers are stripped when redirecting between different subdomains.
    Refines the 'different hostname' check to ensure subdomain boundaries are respected
    to prevent token leakage (e.g., site.example.com to api.example.com).
    """
    session = Session()
    old_url = "http://site.example.com/resource"
    new_url = "http://api.example.com/resource"
    
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is True, "Auth should be stripped when redirecting between different subdomains"