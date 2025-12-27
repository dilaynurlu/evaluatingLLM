import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_strips_authorization_when_unsafe_redirect():
    """
    Test that rebuild_auth removes the 'Authorization' header when 
    should_strip_auth returns True.
    """
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Scenario: Redirect to a host where auth should be stripped.
        # netrc auth is irrelevant for this test, so we disable env trust.
        
        mock_session = Mock()
        mock_session.trust_env = False
        mock_session.should_strip_auth.return_value = True
        
        # Prepare a request with an Authorization header
        headers = {"Authorization": "Basic original_creds"}
        prepared_request = Mock()
        prepared_request.headers = headers
        prepared_request.url = "http://new-host.com/resource"
        
        # Prepare a response from the old URL
        response = Mock()
        response.request.url = "http://old-host.com/resource"
        
        # Call the target function (unbound)
        Session.rebuild_auth(mock_session, prepared_request, response)
        
        # Assertions
        assert "Authorization" not in headers
        mock_session.should_strip_auth.assert_called_once_with(
            "http://old-host.com/resource", 
            "http://new-host.com/resource"
        )