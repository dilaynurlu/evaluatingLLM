import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_strips_authorization_on_redirect_to_different_host():
    """
    Test that Authorization header is removed when redirecting to a different host,
    and no new credentials are found in netrc.
    """
    session = Session()
    # Ensure environment is trusted, though we mock netrc to return None
    session.trust_env = True
    
    # Setup the original request (that received a redirect response)
    # Origin: secure.example.com
    original_req = PreparedRequest()
    original_req.prepare(
        method="GET",
        url="https://secure.example.com/resource"
    )
    
    response = Response()
    response.request = original_req
    
    # Setup the new request (target of the redirect)
    # Target: other.example.com (Different host -> should strip auth)
    # The new request inherits headers from the original by default in requests logic.
    redirected_req = PreparedRequest()
    redirected_req.prepare(
        method="GET",
        url="https://other.example.com/resource",
        headers={"Authorization": "Basic c2VjcmV0OnBhc3N3b3Jk"}
    )
    
    # Access the function under test
    rebuild_auth = Session.rebuild_auth
    
    # Mock get_netrc_auth to return None (no new creds found)
    with patch("requests.sessions.get_netrc_auth", return_value=None):
        rebuild_auth(session, redirected_req, response)
    
    # Assert Authorization header is removed
    assert "Authorization" not in redirected_req.headers