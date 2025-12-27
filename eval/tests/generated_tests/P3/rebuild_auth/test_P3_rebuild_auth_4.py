import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_does_nothing_if_no_netrc_credentials_found():
    """
    Refined test ensures no changes occur if environment is trusted but no credentials exist,
    using robust header structures.
    """
    # Target function access
    rebuild_auth = Session.rebuild_auth
    
    # Setup mocks
    mock_session = MagicMock(spec=Session)
    mock_session.trust_env = True
    mock_session.should_strip_auth.return_value = False
    
    mock_prepared_request = MagicMock()
    # Empty headers, properly typed
    mock_prepared_request.headers = CaseInsensitiveDict({})
    mock_prepared_request.url = "https://public-host.com/resource"
    
    mock_response = MagicMock()
    mock_response.request.url = "https://other.com"

    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        mock_get_netrc.return_value = None
        
        # Execute
        rebuild_auth(mock_session, mock_prepared_request, mock_response)
        
        # Verify
        mock_get_netrc.assert_called_once()
        mock_prepared_request.prepare_auth.assert_not_called()

'''
Manually marked as assertion correct in csv, because test contains a assertion. Just not recognized by the tool
'''