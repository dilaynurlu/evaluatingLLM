import pytest
from requests.sessions import Session

def test_should_strip_auth_strips_on_https_to_http_downgrade():
    session = Session()
    # Scenario: Downgrade from HTTPS to HTTP on the same host.
    # This is insecure, so Authorization headers should be stripped.
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # Check that should_strip_auth returns True (auth is stripped)
    assert session.should_strip_auth(old_url, new_url) is True