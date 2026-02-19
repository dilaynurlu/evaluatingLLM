import pytest
from requests.sessions import Session

def test_should_strip_auth_explicit_to_implicit_default_port():
    """
    Test that authentication is preserved when redirecting from explicit to implicit
    default ports for the same scheme (HTTP).
    """
    session = Session()
    # http explicit (80) -> http implicit (None)
    old_url = "http://example.com:80/page"
    new_url = "http://example.com/page"
    
    # Logic handles default port equivalence.
    assert session.should_strip_auth(old_url, new_url) is False