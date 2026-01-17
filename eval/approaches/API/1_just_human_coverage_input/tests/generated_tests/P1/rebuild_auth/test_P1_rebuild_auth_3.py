import pytest
from requests import Session, Request, Response
from unittest.mock import patch

def test_rebuild_auth_applies_netrc_credentials():
    # Patch the get_netrc_auth function used in requests.sessions
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        # Mock returning credentials for the new URL
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        
        session = Session()
        session.trust_env = True  # Must be True to check netrc
        
        # Original request context
        orig_req = Request("GET", "http://anywhere.com")
        orig_prep = orig_req.prepare()
        
        response = Response()
        response.request = orig_prep
        
        # New request has no auth initially
        new_req = Request("GET", "http://protected.com/resource")
        new_prep = new_req.prepare()
        
        assert "Authorization" not in new_prep.headers
        
        session.rebuild_auth(new_prep, response)
        
        # Verify get_netrc_auth was called with new URL
        mock_netrc.assert_called_with("http://protected.com/resource")
        
        # Verify Authorization header was added
        assert "Authorization" in new_prep.headers
        # "netrc_user:netrc_pass" base64 encoded is "bmV0cmNfdXNlcjpuZXRyY19wYXNz"
        assert new_prep.headers["Authorization"] == "Basic bmV0cmNfdXNlcjpuZXRyY19wYXNz"