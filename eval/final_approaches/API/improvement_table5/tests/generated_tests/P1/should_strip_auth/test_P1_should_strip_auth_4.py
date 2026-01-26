import pytest
from requests.sessions import Session

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that Authorization header is stripped when downgrading from HTTPS to HTTP.
    This ensures credentials are not sent over an insecure connection.
    """
    session = Session()
    old_url = "https://example.com/resource"
    new_url = "http://example.com/resource"
    
    # Scheme changed from secure to insecure, so auth should be stripped
    assert session.should_strip_auth(old_url, new_url) is True