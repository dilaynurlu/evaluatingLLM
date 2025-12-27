import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_no_authorization_header_present():
    """
    Test that rebuild_auth handles the case where Authorization header 
    is missing, even if strip is required. It should simply do nothing 
    regarding stripping and proceed to netrc checks.
    """
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        mock_get_netrc.return_value = None
        
        mock_session = Mock()
        mock_session.trust_env = False
        mock_session.should_strip_auth.return_value = True
        
        # Prepare a request WITHOUT Authorization header
        headers = {"User-Agent": "test-agent"}
        prepared_request = Mock()
        prepared_request.headers = headers
        prepared_request.url = "http://new.com"
        
        response = Mock()
        response.request.url = "http://old.com"
        
        # Call the target function
        Session.rebuild_auth(mock_session, prepared_request, response)
        
        # Assertions
        # should_strip_auth is NOT called because "Authorization" is not in headers
        # Logic: if "Authorization" in headers and self.should_strip_auth(...)
        mock_session.should_strip_auth.assert_not_called()
        
        # Headers should remain unchanged
        assert "Authorization" not in headers
        assert headers["User-Agent"] == "test-agent"