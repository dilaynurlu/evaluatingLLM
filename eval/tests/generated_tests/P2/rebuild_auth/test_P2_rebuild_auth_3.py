import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_applies_netrc_credentials_when_found():
    """
    Test that credentials from .netrc are applied to the request if found,
    assuming trust_env is True.
    """
    session = Session()
    session.trust_env = True
    
    # Original request context
    original_req = PreparedRequest()
    original_req.prepare(
        method="GET",
        url="https://origin.com/"
    )
    
    response = Response()
    response.request = original_req
    
    # Redirected request with NO initial auth
    target_url = "https://internal.com/resource"
    redirected_req = PreparedRequest()
    redirected_req.prepare(
        method="GET",
        url=target_url
    )
    
    rebuild_auth = Session.rebuild_auth
    
    # Mock netrc to return valid credentials for the new URL
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        
        rebuild_auth(session, redirected_req, response)
        
        mock_netrc.assert_called_once_with(target_url)
    
    # Verify Auth header is added
    assert "Authorization" in redirected_req.headers
    # "netrc_user:netrc_pass" -> base64 "bmV0cmNXdXNlcjpuZXRyY19wYXNz"
    # Verification of exact Basic auth string
    assert redirected_req.headers["Authorization"].startswith("Basic ")