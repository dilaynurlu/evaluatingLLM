import pytest
from requests.sessions import Session

def test_should_strip_auth_same_url_different_path():
    """
    Test that Authorization header is preserved when only the path changes
    (same host, scheme, and port).
    """
    session = Session()
    old_url = "http://example.com/old/path"
    new_url = "http://example.com/new/path"
    
    # No change in origin, so auth should NOT be stripped
    assert session.should_strip_auth(old_url, new_url) is False