import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_ignores_netrc_when_untrusted():
    """
    Test that rebuild_auth does NOT query or apply .netrc credentials 
    if session.trust_env is False, ensuring environment isolation.
    """
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        # Mock setup (should effectively be ignored)
        mock_netrc.return_value = ("user", "pass")

        session = Session()
        session.trust_env = False  # Untrusted environment

        original_req = PreparedRequest()
        original_req.url = "http://start.com"
        
        response = Response()
        response.request = original_req

        redirected_req = PreparedRequest()
        redirected_req.url = "http://target.com"
        redirected_req.headers = CaseInsensitiveDict({})

        # Execute
        session.rebuild_auth(redirected_req, response)

        # Verify no auth added
        assert "Authorization" not in redirected_req.headers
        
        # Verify get_netrc_auth was NOT called (optimization and security check)
        mock_netrc.assert_not_called()