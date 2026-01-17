import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response
from requests.auth import HTTPBasicAuth

def test_rebuild_auth_strips_old_auth_and_applies_netrc():
    """
    Test the scenario where authentication is stripped due to a host change,
    but new authentication is immediately applied from netrc for the new host.
    """
    session = Session()
    session.trust_env = True
    
    # Old request with original credentials
    old_url = "http://old-host.com"
    original_req = Request("GET", old_url, auth=("old_user", "old_pass")).prepare()
    
    response = Response()
    response.request = original_req
    
    # New request to different host
    new_url = "http://new-host.com"
    new_req = Request("GET", new_url).prepare()
    
    # Initially, new_req has the old headers (copied by logic before rebuild_auth)
    new_req.headers["Authorization"] = original_req.headers["Authorization"]
    
    # Verify we start with old auth
    old_auth_header = original_req.headers["Authorization"]
    assert new_req.headers["Authorization"] == old_auth_header
    
    # Netrc has credentials for the NEW host
    netrc_creds = ("new_user", "new_pass")
    
    with patch("requests.sessions.get_netrc_auth", return_value=netrc_creds):
        session.rebuild_auth(new_req, response)
        
    # Assert the old authorization is gone and replaced by the new one
    assert "Authorization" in new_req.headers
    assert new_req.headers["Authorization"] != old_auth_header
    
    expected_new_header = HTTPBasicAuth(*netrc_creds)(Request()).headers["Authorization"]
    assert new_req.headers["Authorization"] == expected_new_header