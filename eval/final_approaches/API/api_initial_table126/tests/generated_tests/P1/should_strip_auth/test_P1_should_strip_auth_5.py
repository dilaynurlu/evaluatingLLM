import pytest
from requests.sessions import Session

def test_should_strip_auth_on_non_standard_port_change():
    """
    Test that Authorization header is stripped if the port changes to a non-default value.
    """
    session = Session()
    old_url = "http://example.com:8080/foo"
    new_url = "http://example.com:9090/foo"
    
    # Logic:
    # Hostnames match.
    # changed_port is True.
    # Default port check fails (8080 not in defaults).
    # Returns True.
    assert session.should_strip_auth(old_url, new_url) is True