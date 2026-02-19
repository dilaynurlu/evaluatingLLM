import pytest
from requests.sessions import Session

def test_should_strip_auth_port_change_non_default():
    """
    Test that Authorization header is stripped when ports change 
    and are not equivalent default ports.
    Matches return: changed_port or changed_scheme
    """
    session = Session()
    old_url = "http://example.com:8080/api"
    new_url = "http://example.com:9090/api"
    
    # Port change -> should strip auth
    assert session.should_strip_auth(old_url, new_url) is True