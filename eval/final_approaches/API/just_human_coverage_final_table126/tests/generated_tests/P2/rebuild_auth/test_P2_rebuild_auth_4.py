import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_ignores_netrc_when_trust_env_is_false():
    """
    Test that .netrc lookup is skipped if session.trust_env is False,
    ensuring no credentials are inadvertently applied.
    """
    session = Session()
    session.trust_env = False
    
    original_req = PreparedRequest()
    original_req.prepare(
        method="GET",
        url="https://origin.com/"
    )
    
    response = Response()
    response.request = original_req
    
    # Redirected request to a new host
    redirected_req = PreparedRequest()
    redirected_req.prepare(
        method="GET",
        url="https://target.com/resource"
    )
    
    rebuild_auth = Session.rebuild_auth
    
    # Mock netrc - should NOT be accessed
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("user", "pass")
        
        rebuild_auth(session, redirected_req, response)
        
        # Verify get_netrc_auth was never called
        mock_netrc.assert_not_called()
    
    # Verify no auth header added
    assert "Authorization" not in redirected_req.headers