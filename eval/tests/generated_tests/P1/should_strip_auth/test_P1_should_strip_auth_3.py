import pytest
from requests.sessions import Session

def test_should_strip_auth_on_scheme_downgrade():
    """
    Test that Authorization header is stripped when redirecting from HTTPS to HTTP.
    This is a security downgrade.
    """
    session = Session()
    old_url = "https://example.com/secret"
    new_url = "http://example.com/secret"
    
    # Logic:
    # Hostnames match.
    # Special upgrade case (http->https) does NOT match.
    # Default port logic: schemes differ -> not covered.
    # Returns changed_port or changed_scheme -> changed_scheme is True.
    assert session.should_strip_auth(old_url, new_url) is True