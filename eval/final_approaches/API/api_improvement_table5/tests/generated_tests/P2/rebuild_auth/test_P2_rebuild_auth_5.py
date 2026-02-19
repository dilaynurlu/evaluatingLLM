import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict
from requests.auth import _basic_auth_str
from unittest.mock import patch

def test_rebuild_auth_host_change_with_new_netrc():
    """
    Test a complex scenario where:
    1. A redirect occurs to a different host (should strip old auth).
    2. The new host has credentials in .netrc (should apply new auth).
    """
    session = Session()
    session.trust_env = True
    
    # 1. Setup original request (Old Host)
    original_req = PreparedRequest()
    original_req.url = "https://old-host.com/resource"
    
    response = Response()
    response.request = original_req
    
    # 2. Setup new request (New Host)
    # It starts with the Old Host's auth (simulating carried-over headers)
    new_req = PreparedRequest()
    new_req.url = "https://new-host.com/resource"
    new_req.headers = CaseInsensitiveDict({
        "Authorization": "Basic b2xkOmNyZWQ=" # old:cred
    })
    
    # 3. Mock netrc to return credentials for the NEW host
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        mock_get_netrc.return_value = ("newuser", "newpass")
        
        # Call target function
        session.rebuild_auth(new_req, response)
        
        mock_get_netrc.assert_called_with("https://new-host.com/resource")
        
        # 4. Verification
        # Old header should be gone, replaced by new header
        assert "Authorization" in new_req.headers
        
        expected_new_auth = _basic_auth_str("newuser", "newpass")
        assert new_req.headers["Authorization"] == expected_new_auth
        
        # Explicit check that it's not the old one
        assert new_req.headers["Authorization"] != "Basic b2xkOmNyZWQ="