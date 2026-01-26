import requests
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict
from unittest.mock import patch

def test_rebuild_auth_ignores_netrc_when_untrusted():
    """
    Test that rebuild_auth does NOT query .netrc or apply credentials
    when trust_env is False, even if credentials exist.
    """
    session = Session()
    session.trust_env = False
    
    # 1. Setup original request
    original_req = PreparedRequest()
    original_req.url = "https://example.com/"
    
    response = Response()
    response.request = original_req
    
    # 2. Setup new request
    new_req = PreparedRequest()
    new_req.url = "https://private.com/"
    new_req.headers = CaseInsensitiveDict()
    
    # 3. Mock get_netrc_auth to ensure it's not effectively used
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        mock_get_netrc.return_value = ("user", "pass")
        
        # Call target function
        session.rebuild_auth(new_req, response)
        
        # 4. Verification
        # Depending on implementation, get_netrc_auth might be skipped entirely or ignored
        # The key result is that no header is added.
        assert "Authorization" not in new_req.headers