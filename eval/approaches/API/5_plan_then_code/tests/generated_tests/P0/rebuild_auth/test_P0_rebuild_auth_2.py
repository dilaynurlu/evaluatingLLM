import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_preserves_authorization_when_not_stripped():
    """
    Test that rebuild_auth retains the 'Authorization' header when should_strip_auth returns False.
    """
    session = Session()
    session.trust_env = False

    # Create a PreparedRequest with an existing Authorization header
    req = PreparedRequest()
    req.prepare(
        method="GET",
        url="http://same-host.com/resource",
        headers={"Authorization": "Basic keep_these_credentials"}
    )

    # Mock the original response and its request
    original_req = PreparedRequest()
    original_req.prepare(method="GET", url="http://same-host.com/resource")
    
    resp = Response()
    resp.request = original_req

    # Mock should_strip_auth to return False (e.g., same host redirect)
    with patch.object(session, 'should_strip_auth', return_value=False):
        session.rebuild_auth(req, resp)
        
        # Verify header is still present and unchanged
        assert "Authorization" in req.headers
        assert req.headers["Authorization"] == "Basic keep_these_credentials"