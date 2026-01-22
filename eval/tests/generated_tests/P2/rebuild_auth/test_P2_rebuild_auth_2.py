import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_retains_authorization_on_redirect_to_same_host():
    """
    Test that Authorization header is preserved when redirecting to the same host,
    provided netrc does not override it.
    """
    session = Session()
    
    # Setup original request
    original_req = PreparedRequest()
    original_req.prepare(
        method="GET",
        url="https://example.com/page1"
    )
    
    response = Response()
    response.request = original_req
    
    # Setup redirected request to the SAME host
    # Same host -> should NOT strip auth
    auth_header = "Basic c2VjcmV0OnBhc3N3b3Jk"
    redirected_req = PreparedRequest()
    redirected_req.prepare(
        method="GET",
        url="https://example.com/page2",
        headers={"Authorization": auth_header}
    )
    
    rebuild_auth = Session.rebuild_auth
    
    # Mock netrc to return None so it doesn't overwrite existing auth
    with patch("requests.sessions.get_netrc_auth", return_value=None):
        rebuild_auth(session, redirected_req, response)
    
    # Assert Authorization header is retained
    assert "Authorization" in redirected_req.headers
    assert redirected_req.headers["Authorization"] == auth_header