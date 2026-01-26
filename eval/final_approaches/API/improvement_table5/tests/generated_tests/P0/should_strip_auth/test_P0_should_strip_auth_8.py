import pytest
from requests.sessions import Session

def test_should_strip_auth_same_url_no_change():
    """
    Test that authentication is preserved when the URL authority components (scheme, host, port)
    do not change.
    """
    session = Session()
    old_url = "http://example.com/foo?q=1"
    new_url = "http://example.com/foo?q=2"
    
    # No change in scheme, host, or port.
    assert session.should_strip_auth(old_url, new_url) is False