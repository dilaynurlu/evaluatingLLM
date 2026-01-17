import pytest
from requests import Session

def test_should_strip_auth_port_change_same_scheme():
    """
    Test that Authorization headers are stripped when the port changes 
    (and neither is a default port alias of the other).
    """
    session = Session()
    old_url = "http://example.com:8080/api"
    new_url = "http://example.com:9090/api"
    
    # Expect True because the port has changed significantly
    assert session.should_strip_auth(old_url, new_url) is True