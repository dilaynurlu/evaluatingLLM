from requests.sessions import Session

def test_should_not_strip_auth_explicit_to_implicit_https_port():
    """
    Test that auth is preserved when redirecting from explicit port 443 to implicit https.
    """
    session = Session()
    old_url = "https://example.com:443/resource"
    new_url = "https://example.com/resource"
    
    # Explicit 443 and implicit None are treated as equal for 'https' scheme.
    # default_port logic -> return False
    assert session.should_strip_auth(old_url, new_url) is False