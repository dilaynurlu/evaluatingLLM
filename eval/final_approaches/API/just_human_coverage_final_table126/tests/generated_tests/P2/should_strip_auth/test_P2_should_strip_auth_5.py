import requests

def test_should_strip_auth_https_implicit_explicit_port_match():
    """
    Test that Authorization header is NOT stripped when moving between implicit and explicit default ports.
    https://host and https://host:443 are effectively the same origin.
    """
    session = requests.Session()
    # Implicit port (None) matches explicit default port (443) for HTTPS
    assert not session.should_strip_auth("https://example.com/foo", "https://example.com:443/bar")