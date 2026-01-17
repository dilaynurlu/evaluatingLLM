import pytest
from unittest.mock import patch, Mock
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_strips_authorization_on_redirect_when_required():
    """
    Test that rebuild_auth removes the 'Authorization' header when should_strip_auth returns True.
    """
    session = Session()
    # Disable trust_env so netrc logic doesn't interfere/add back headers
    session.trust_env = False

    # Create a PreparedRequest with an existing Authorization header
    req = PreparedRequest()
    req.prepare(
        method="GET",
        url="http://new-host.com/resource",
        headers={"Authorization": "Basic old_credentials"}
    )

    # Mock the original response and its request
    original_req = PreparedRequest()
    original_req.prepare(method="GET", url="http://old-host.com/resource")
    
    resp = Response()
    resp.request = original_req

    # Mock should_strip_auth to force return True indicating auth should be stripped
    with patch.object(session, 'should_strip_auth', return_value=True) as mock_should_strip:
        session.rebuild_auth(req, resp)
        
        # Verify interactions and state
        mock_should_strip.assert_called_with("http://old-host.com/resource", "http://new-host.com/resource")
        assert "Authorization" not in req.headers