import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict
from requests.auth import _basic_auth_str
from unittest.mock import patch

def test_rebuild_auth_applies_netrc_auth():
    """
    Test that rebuild_auth queries .netrc and applies credentials
    when trust_env is True and credentials are found for the new host.
    """
    session = Session()
    session.trust_env = True
    
    # 1. Setup original request
    original_req = PreparedRequest()
    original_req.url = "https://public.com/"
    
    response = Response()
    response.request = original_req
    
    # 2. Setup new request (target host needs auth)
    new_req = PreparedRequest()
    new_req.url = "https://private.com/resource"
    new_req.headers = CaseInsensitiveDict()  # No auth initially
    
    # 3. Mock get_netrc_auth to simulate finding credentials
    # We patch it in requests.sessions where it is imported
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        mock_get_netrc.return_value = ("myuser", "mypassword")
        
        # Call target function
        session.rebuild_auth(new_req, response)
        
        # Verify call arguments
        mock_get_netrc.assert_called_with("https://private.com/resource")
        
        # Verify Authorization header is added correctly
        assert "Authorization" in new_req.headers
        expected_header = _basic_auth_str("myuser", "mypassword")
        assert new_req.headers["Authorization"] == expected_header