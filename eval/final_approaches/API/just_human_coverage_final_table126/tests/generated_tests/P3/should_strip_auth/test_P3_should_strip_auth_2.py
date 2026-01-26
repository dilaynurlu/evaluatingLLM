import pytest
from requests.sessions import Session

def test_should_strip_auth_allows_safe_http_to_https_upgrade():
    session = Session()
    # Scenario 1: Standard upgrade on same host.
    assert session.should_strip_auth("http://example.com/login", "https://example.com/login") is False
    
    # Scenario 2: Case Insensitivity (Critique 2).
    # Hostnames are case-insensitive. A redirect to an uppercase version of the same host 
    # should be considered the same host and allow the safe upgrade logic to pass.
    assert session.should_strip_auth("http://example.com/login", "https://EXAMPLE.COM/login") is False
    
    # Scenario 3: Mixed case consistency.
    assert session.should_strip_auth("http://ExAmPlE.CoM/login", "https://eXaMpLe.cOm/login") is False