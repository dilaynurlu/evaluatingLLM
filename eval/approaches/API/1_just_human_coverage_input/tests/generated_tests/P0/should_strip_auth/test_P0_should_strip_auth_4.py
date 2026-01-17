import requests

def test_should_strip_auth_port_change_non_standard():
    """
    Test that Authorization header is stripped when changing ports on the same scheme,
    if the ports are not the default ports for that scheme.
    """
    session = requests.Session()
    old_url = "http://example.com:8080/api"
    new_url = "http://example.com:9090/api"
    
    # Expect True because ports changed and they are not standard default ports
    assert session.should_strip_auth(old_url, new_url) is True