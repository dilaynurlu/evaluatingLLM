import requests
from requests.sessions import Session
from requests.models import Response, Request
from unittest.mock import patch

def test_rebuild_auth_applies_netrc_auth_when_trusted_env():
    session = Session()
    # Enable trust_env to allow .netrc lookups
    session.trust_env = True
    
    original_url = "http://example.com/old"
    original_req = Request("GET", original_url).prepare()
    
    response = Response()
    response.request = original_req
    
    target_url = "http://example.com/new"
    # Create request without existing auth
    target_req = Request("GET", target_url).prepare()
    assert "Authorization" not in target_req.headers
    
    # Mock get_netrc_auth to return credentials for the target URL
    # We patch where it is imported in requests.sessions
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        mock_netrc.return_value = ("netrc_user", "netrc_pass")
        
        session.rebuild_auth(target_req, response)
        
        # Ensure it queried netrc for the new URL
        mock_netrc.assert_called_with(target_url)
        
    # Verify Authorization header was added
    assert "Authorization" in target_req.headers
    # "netrc_user:netrc_pass" base64 encoded is "bmV0cmNfdXNlcjpuZXRyY19wYXNz"
    expected_auth = "Basic bmV0cmNfdXNlcjpuZXRyY19wYXNz"
    assert target_req.headers["Authorization"] == expected_auth