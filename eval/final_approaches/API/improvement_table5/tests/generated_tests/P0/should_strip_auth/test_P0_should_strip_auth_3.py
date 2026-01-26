import pytest
from requests.sessions import Session

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that authentication is stripped when redirecting from HTTPS to HTTP (downgrade).
    """
    session = Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # Scheme change https -> http is not exempted.
    assert session.should_strip_auth(old_url, new_url) is True