import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.auth import _basic_auth_str

def test_rebuild_auth_strips_old_and_applies_new_netrc_auth():
    """
    Test that credentials are stripped when downgrading protocol (HTTPS -> HTTP),
    but new credentials from .netrc are applied if available.
    
    Refinements based on critique:
    - Tests the specific security flaw of Protocol Downgrade (HTTPS to HTTP).
    - Verifies that even on the same host, downgrading security strips original auth.
    """
    session = Session()
    
    # Original request was HTTPS
    original_req = PreparedRequest()
    original_req.prepare(method="GET", url="https://example.com/secure")
    
    response = Response()
    response.request = original_req
    
    # New request is HTTP (Protocol Downgrade) but same host
    # Carrying over old credentials initially
    new_req = PreparedRequest()
    new_req.prepare(
        method="GET", 
        url="http://example.com/insecure", 
        headers={"Authorization": "Basic old_secure_creds"}
    )
    
    # Mock netrc to return credentials suitable for the insecure endpoint (if allowed)
    new_user, new_pass = "insecure_user", "insecure_pass"
    with patch("requests.sessions.get_netrc_auth", return_value=(new_user, new_pass)):
        session.rebuild_auth(new_req, response)
    
    # Assertion 1: Old secure credentials must be stripped due to protocol downgrade
    current_auth = new_req.headers.get("Authorization")
    assert "old_secure_creds" not in str(current_auth)
    
    # Assertion 2: New credentials should be applied (since netrc was found)
    expected_auth = _basic_auth_str(new_user, new_pass)
    assert current_auth == expected_auth