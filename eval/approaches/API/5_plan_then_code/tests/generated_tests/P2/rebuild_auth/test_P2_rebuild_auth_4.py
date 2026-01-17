import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_respects_trust_env_false():
    """
    Test that rebuild_auth does NOT apply netrc credentials if trust_env is False,
    even if they exist.
    """
    session = Session()
    session.trust_env = False
    
    original_req = Request("GET", "http://example.com").prepare()
    response = Response()
    response.request = original_req
    
    new_url = "http://target.com/resource"
    new_req = Request("GET", new_url).prepare()
    
    assert "Authorization" not in new_req.headers
    
    # Even if get_netrc_auth would return something, it shouldn't be called or used
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("user", "pass")
        
        session.rebuild_auth(new_req, response)
        
        # Verify get_netrc_auth was NOT called because trust_env is False
        mock_netrc.assert_not_called()
    
    assert "Authorization" not in new_req.headers