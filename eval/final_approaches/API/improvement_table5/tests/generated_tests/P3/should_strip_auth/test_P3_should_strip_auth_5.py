from requests.sessions import Session

def test_should_strip_auth_default_port_equivalence():
    """
    Test that authentication is preserved when redirecting between implicit
    and explicit default ports.
    Refined to cover both HTTP (80) and HTTPS (443).
    """
    session = Session()
    
    # HTTP Default (None vs 80)
    assert session.should_strip_auth("http://example.com/a", "http://example.com:80/a") is False
    assert session.should_strip_auth("http://example.com:80/a", "http://example.com/a") is False
    
    # HTTPS Default (None vs 443)
    assert session.should_strip_auth("https://example.com/b", "https://example.com:443/b") is False
    assert session.should_strip_auth("https://example.com:443/b", "https://example.com/b") is False