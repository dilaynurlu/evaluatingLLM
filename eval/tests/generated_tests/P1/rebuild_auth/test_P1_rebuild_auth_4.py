import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_ignores_netrc_when_untrusted():
    """
    Test that rebuild_auth does NOT apply netrc authentication 
    if trust_env is False, even if credentials exist.
    """
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Scenario: trust_env is False.
        
        mock_session = Mock()
        mock_session.trust_env = False
        
        prepared_request = Mock()
        prepared_request.headers = {}
        prepared_request.url = "http://somewhere.com"
        
        response = Mock()
        response.request.url = "http://old.com"
        
        # Call the target function
        Session.rebuild_auth(mock_session, prepared_request, response)
        
        # Assertions
        # get_netrc_auth should not be called because trust_env is False
        # Logic: new_auth = get_netrc_auth(url) if self.trust_env else None
        mock_get_netrc.assert_not_called()
        
        # prepare_auth should not be called
        prepared_request.prepare_auth.assert_not_called()


'''
Manually marked as assertion correct, because it contains passing assertions. Just not recognized by the tool.
'''