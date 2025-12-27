import pytest
from requests.sessions import Session

def test_should_strip_auth_enforces_strip_on_https_to_http_downgrade():
    """
    Test that Authorization headers are STRIPPED when downgrading from 
    HTTPS to HTTP, even on the same host. This prevents leaking credentials 
    over plaintext.
    """
    session = Session()
    old_url = "https://example.com/secure"
    new_url = "http://example.com/secure"
    
    # Logic:
    # Hostname match.
    # Special case (http->https) does NOT match.
    # changed_scheme is True.
    # Not handled by default port logic (since scheme changed and it's not the exception).
    # Returns changed_port or changed_scheme -> True.
    result = session.should_strip_auth(old_url, new_url)
    
    assert result is True, "Auth should be stripped when downgrading https -> http"