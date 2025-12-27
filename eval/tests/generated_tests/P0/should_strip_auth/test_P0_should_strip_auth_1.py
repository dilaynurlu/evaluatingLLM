import pytest
from requests.sessions import Session

def test_should_strip_auth_hostname_mismatch():
    session = Session()
    old_url = "http://example.com/resource"
    new_url = "http://other-domain.com/resource"
    
    # Scenario: The hostname changes during redirect.
    # Expected behavior: Authorization headers should be stripped (return True).
    assert session.should_strip_auth(old_url, new_url) is True