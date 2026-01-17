import requests
from requests.sessions import Session

def test_should_strip_auth_implicit_and_explicit_default_ports():
    """
    Test that Authorization header is preserved when redirecting between implicit 
    and explicit default ports in both directions.
    """
    session = Session()
    
    # HTTP: Implicit (80) -> Explicit (80)
    assert session.should_strip_auth("http://example.com/r", "http://example.com:80/r") is False
    
    # HTTP: Explicit (80) -> Implicit (80)
    assert session.should_strip_auth("http://example.com:80/r", "http://example.com/r") is False
    
    # HTTPS: Implicit (443) -> Explicit (443)
    assert session.should_strip_auth("https://example.com/r", "https://example.com:443/r") is False
    
    # HTTPS: Explicit (443) -> Implicit (443)
    assert session.should_strip_auth("https://example.com:443/r", "https://example.com/r") is False