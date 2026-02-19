import pytest
from requests.sessions import Session

def test_should_strip_auth_implicit_to_explicit_default_port():
    """
    Test that authentication is preserved when redirecting from implicit to explicit
    default ports for the same scheme (HTTP).
    """
    session = Session()
    # http implicit (None) -> http explicit (80)
    old_url = "http://example.com/page"
    new_url = "http://example.com:80/page"
    
    # Ports differ technically (None vs 80), but logic handles default port equivalence.
    assert session.should_strip_auth(old_url, new_url) is False