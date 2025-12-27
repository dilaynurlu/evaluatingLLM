import pytest
from requests.sessions import Session

def test_should_strip_auth_https_to_http_downgrade():
    session = Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # Scenario: Downgrading from HTTPS to HTTP (insecure redirect).
    # Expected behavior: Authorization headers should be stripped (return True).
    assert session.should_strip_auth(old_url, new_url) is True