import pytest
from requests import Session

def test_should_strip_auth_mixed_explicit_implicit_default_ports():
    """
    Test that Authorization headers are NOT stripped when the port changes only
    between implicit default and explicit default (e.g., :80 vs implied 80).
    """
    session = Session()
    # old_url uses implicit port 80 for http
    old_url = "http://example.com/page"
    # new_url uses explicit port 80 for http
    new_url = "http://example.com:80/page"
    
    # Expect False because both effectively refer to port 80 on the same scheme
    assert session.should_strip_auth(old_url, new_url) is False