import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_strips_old_token_and_applies_netrc_on_cross_domain_redirect():
    """
    Refined integration-style test covering the interaction:
    1. Strip sensitive header from Host A.
    2. Apply new credentials from .netrc for Host B.
    """
    # Target function access
    rebuild_auth = Session.rebuild_auth
    
    # Setup mocks
    mock_session = MagicMock(spec=Session)
    mock_session.trust_env = True
    # Scenario: Redirecting to a new domain requires stripping the old auth
    mock_session.should_strip_auth.return_value = True
    
    mock_prepared_request = MagicMock()
    # Old auth for the previous host
    mock_prepared_request.headers = CaseInsensitiveDict({"Authorization": "Basic old_secret"})
    mock_prepared_request.url = "https://new-host.com/resource"
    
    mock_response = MagicMock()
    mock_response.request.url = "https://old-host.com/resource"

    # Patch get_netrc_auth
    with patch("requests.sessions.get_netrc_auth") as mock_get_netrc:
        # Define credentials for the NEW host
        mock_auth_tuple = ("user", "password")
        mock_get_netrc.return_value = mock_auth_tuple
        
        # Execute
        rebuild_auth(mock_session, mock_prepared_request, mock_response)
        
        # Verify 1: Old header must be gone
        assert "Authorization" not in mock_prepared_request.headers
        
        # Verify 2: New credentials must be looked up for the NEW url
        mock_get_netrc.assert_called_once_with("https://new-host.com/resource")
        
        # Verify 3: New credentials applied
        mock_prepared_request.prepare_auth.assert_called_once_with(mock_auth_tuple)