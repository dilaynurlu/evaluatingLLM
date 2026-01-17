import pytest
from requests import Session, Request, Response
from unittest.mock import patch

def test_rebuild_auth_strips_stale_auth_and_applies_netrc():
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("new_user", "new_pass")
        
        session = Session()
        session.trust_env = True
        
        # Cross-host scenario: triggers stripping
        orig_req = Request("GET", "http://host-a.com/path")
        orig_prep = orig_req.prepare()
        
        response = Response()
        response.request = orig_prep
        
        # The new request has "stale" auth copied from original
        new_req = Request("GET", "http://host-b.com/path", 
                          headers={"Authorization": "Basic stale_token"})
    
        new_prep = new_req.prepare()
        
        # Ensure we start with Authorization
        assert new_prep.headers["Authorization"] == "Basic stale_token"
        
        session.rebuild_auth(new_prep, response)
        
        # The "stale_token" should be gone (stripped due to host change)
        # And "new_user:new_pass" should be present (from netrc)
        
        assert "Authorization" in new_prep.headers
        assert new_prep.headers["Authorization"] != "Basic stale_token"
        # "new_user:new_pass" -> bmV3X3VzZXI6bmV3X3Bhc3M=
        assert new_prep.headers["Authorization"] == "Basic bmV3X3VzZXI6bmV3X3Bhc3M="