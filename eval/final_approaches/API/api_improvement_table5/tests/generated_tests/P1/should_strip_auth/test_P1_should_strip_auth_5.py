import pytest
from requests.sessions import Session

def test_should_strip_auth_port_change():
    """
    Test that Authorization header is stripped when the port changes to a non-default port
    on the same host and scheme.
    """
    session = Session()
    old_url = "http://example.com:8080/resource"
    new_url = "http://example.com:9090/resource"
    
    # Port changed, so auth should be stripped
    assert session.should_strip_auth(old_url, new_url) is True