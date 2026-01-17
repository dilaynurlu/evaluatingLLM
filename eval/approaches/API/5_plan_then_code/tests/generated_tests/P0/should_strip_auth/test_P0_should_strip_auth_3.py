import pytest
from requests import Session

def test_should_strip_auth_https_to_http_downgrade():
    """
    Test that Authorization headers are stripped when downgrading from HTTPS to HTTP.
    This does not match the special exception for upgrades.
    """
    session = Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/insecure"
    
    # Expect True because scheme changed and it is not the allowed http->https upgrade
    assert session.should_strip_auth(old_url, new_url) is True