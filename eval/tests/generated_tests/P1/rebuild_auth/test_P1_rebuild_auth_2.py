import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_keeps_authorization_when_safe_redirect():
    """
    Test that rebuild_auth preserves the 'Authorization' header when 
    should_strip_auth returns False.
    """
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Scenario: Redirect to a host where auth should be kept.
        
        mock_session = Mock()
        mock_session.trust_env = False
        mock_session.should_strip_auth.return_value = False
        
        # Prepare a request with an Authorization header
        headers = {"Authorization": "Basic original_creds"}
        prepared_request = Mock()
        prepared_request.headers = headers
        prepared_request.url = "http://same-host.com/new_path"
        
        # Prepare a response from the old URL
        response = Mock()
        response.request.url = "http://same-host.com/old_path"
        
        # Call the target function (unbound)
        Session.rebuild_auth(mock_session, prepared_request, response)
        
        # Assertions
        assert "Authorization" in headers
        assert headers["Authorization"] == "Basic original_creds"
        mock_session.should_strip_auth.assert_called_once()