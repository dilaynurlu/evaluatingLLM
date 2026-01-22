import pytest
from requests.sessions import Session

def test_should_strip_auth_preserves_on_same_origin():
    """
    Test that Authorization header is preserved when host, scheme, and port remain effectively the same,
    even if path or query params change.
    """
    session = Session()
    old_url = "http://example.com/foo"
    new_url = "http://example.com/bar?query=123"
    
    # Logic:
    # Hostnames match.
    # changed_port is False.
    # changed_scheme is False.
    # Returns False.
    assert session.should_strip_auth(old_url, new_url) is False