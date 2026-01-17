import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_ignores_netrc_when_untrusted():
    """
    Test that rebuild_auth does NOT apply .netrc credentials if trust_env is False.
    """
    session = Session()
    session.trust_env = False
    
    original_req = PreparedRequest()
    original_req.prepare(method="GET", url="http://example.com/source")
    
    response = Response()
    response.request = original_req
    
    new_req = PreparedRequest()
    new_req.prepare(method="GET", url="http://example.com/target")
    
    # Mock get_netrc_auth to return credentials
    with patch("requests.sessions.get_netrc_auth", return_value=("user", "pass")):
        session.rebuild_auth(new_req, response)
    
    # Assertion: Authorization header should NOT be present
    assert "Authorization" not in new_req.headers