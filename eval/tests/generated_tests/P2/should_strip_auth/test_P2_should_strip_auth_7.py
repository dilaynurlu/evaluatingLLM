import requests

def test_should_strip_auth_on_default_to_custom_port_change():
    """
    Test that auth is stripped when moving from a default port (implicit)
    to a custom explicit port on the same scheme.
    """
    session = requests.Session()
    old_url = "http://example.com/foo"
    new_url = "http://example.com:8080/foo"
    
    # Implicit 80 vs Explicit 8080. Ports differ -> strip auth.
    assert session.should_strip_auth(old_url, new_url) is True