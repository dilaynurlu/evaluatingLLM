import requests
from requests.sessions import Session
from requests.models import Response, Request
from unittest.mock import patch

def test_rebuild_auth_ignores_netrc_when_trust_env_is_false():
    session = Session()
    # Disable trust_env
    session.trust_env = False
    
    original_url = "http://example.com/old"
    original_req = Request("GET", original_url).prepare()
    
    response = Response()
    response.request = original_req
    
    target_url = "http://example.com/new"
    target_req = Request("GET", target_url).prepare()
    
    # Even if get_netrc_auth were to return credentials, they should not be used
    # Note: Logic usually skips calling get_netrc_auth entirely if trust_env is False
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("user", "pass")
        
        session.rebuild_auth(target_req, response)
        
        # In current implementation, get_netrc_auth is called conditionally:
        # new_auth = get_netrc_auth(url) if self.trust_env else None
        # So mock shouldn't even be called.
        assert not mock_netrc.called
        
    assert "Authorization" not in target_req.headers