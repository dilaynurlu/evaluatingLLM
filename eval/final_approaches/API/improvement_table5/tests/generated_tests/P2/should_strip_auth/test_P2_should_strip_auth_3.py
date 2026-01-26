import pytest
from requests.sessions import Session

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that Authorization header is stripped when downgrading from HTTPS to HTTP.
    This falls through the special case check and hits the changed_scheme check.
    """
    session = Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # Downgrade scheme -> should strip auth for security
    assert session.should_strip_auth(old_url, new_url) is True