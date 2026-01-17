import requests

def test_should_strip_auth_explicit_port_change():
    """
    Test that Authorization headers are stripped when the port changes 
    to a non-equivalent value on the same scheme.
    """
    session = requests.Session()
    
    old_url = "http://example.com:8080/api"
    new_url = "http://example.com:9090/api"
    
    # Logic: Same scheme, same host, but different non-default ports.
    # changed_port is True, and default port logic does not apply.
    assert session.should_strip_auth(old_url, new_url) is True