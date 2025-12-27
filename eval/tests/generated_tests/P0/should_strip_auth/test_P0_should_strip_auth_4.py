import pytest
from requests.sessions import Session

def test_should_strip_auth_port_change_non_standard():
    session = Session()
    old_url = "http://example.com:8080/api"
    new_url = "http://example.com:9090/api"
    
    # Scenario: Redirecting to a different non-standard port on the same host.
    # Expected behavior: Authorization headers should be stripped (return True).
    assert session.should_strip_auth(old_url, new_url) is True