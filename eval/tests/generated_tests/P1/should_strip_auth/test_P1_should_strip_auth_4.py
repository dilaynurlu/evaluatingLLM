import pytest
from requests.sessions import Session

def test_should_strip_auth_on_custom_port_change():
    """
    Test that Authorization headers are STRIPPED when the port changes 
    on the same host (non-default ports).
    """
    session = Session()
    old_url = "http://example.com:8080/resource"
    new_url = "http://example.com:9090/resource"
    
    # Logic:
    # Hostname match.
    # changed_port is True.
    # Not default ports.
    # Returns True.
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is True, "Auth should be stripped when port changes"