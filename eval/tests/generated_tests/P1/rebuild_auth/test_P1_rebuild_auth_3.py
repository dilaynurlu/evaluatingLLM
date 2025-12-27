import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_applies_netrc_auth_when_trusted():
    """
    Test that rebuild_auth applies new authentication from netrc 
    if trust_env is True and credentials are found.
    """
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Scenario: trust_env is True, netrc has creds for the new URL.
        new_auth_creds = ("user", "pass")
        mock_get_netrc.return_value = new_auth_creds
        
        mock_session = Mock()
        mock_session.trust_env = True
        # Strip logic is irrelevant here, set to False to focus on addition
        mock_session.should_strip_auth.return_value = False
        
        headers = {}
        prepared_request = Mock()
        prepared_request.headers = headers
        prepared_request.url = "http://netrc-host.com"
        
        response = Mock()
        response.request.url = "http://old-host.com"
        
        # Call the target function
        Session.rebuild_auth(mock_session, prepared_request, response)
        
        # Assertions
        mock_get_netrc.assert_called_once_with("http://netrc-host.com")
        prepared_request.prepare_auth.assert_called_once_with(new_auth_creds)

'''
Manually marked as assertion correct, because it contains passing assertions. Just not recognized by the tool.
'''