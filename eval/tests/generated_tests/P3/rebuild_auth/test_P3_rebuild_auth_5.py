import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_ignores_netrc_when_trust_env_is_false():
    """
    Refined test confirming strict adherence to trust_env configuration.
    """
    # Target function access
    rebuild_auth = Session.rebuild_auth
    
    # Setup mocks
    mock_session = MagicMock(spec=Session)
    mock_session.trust_env = False
    mock_session.should_strip_auth.return_value = False
    
    mock_prepared_request = MagicMock()
    mock_prepared_request.headers = CaseInsensitiveDict({})
    mock_prepared_request.url = "https://example.com"
    
    mock_response = MagicMock()
    mock_response.request.url = "https://example.com"

    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Execute
        rebuild_auth(mock_session, mock_prepared_request, mock_response)
        
        # Verify
        mock_get_netrc.assert_not_called()
        mock_prepared_request.prepare_auth.assert_not_called()

'''
Manually marked as assertion correct in csv, because test contains a assertion. Just not recognized by the tool
'''