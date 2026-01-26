import pytest
from requests.sessions import Session

def test_should_strip_auth_port_change():
    """
    Test that authentication is stripped when redirecting to a different non-default port.
    """
    session = Session()
    old_url = "http://example.com:8080/api"
    new_url = "http://example.com:9090/api"
    
    # Same scheme, same host, but different ports -> strip auth
    assert session.should_strip_auth(old_url, new_url) is True