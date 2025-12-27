import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_handles_missing_authorization_header_safely():
    """
    Refined test ensuring robustness when stripping is requested but the header 
    does not exist, utilizing CaseInsensitiveDict for realism.
    """
    # Target function access
    rebuild_auth = Session.rebuild_auth
    
    # Setup mocks
    mock_session = MagicMock(spec=Session)
    mock_session.trust_env = False
    # Stripping requested
    mock_session.should_strip_auth.return_value = True
    
    mock_prepared_request = MagicMock()
    # Headers dict does not contain "Authorization"
    mock_prepared_request.headers = CaseInsensitiveDict({"Content-Type": "application/json"})
    mock_prepared_request.url = "https://new.com"
    
    mock_response = MagicMock()
    mock_response.request.url = "https://old.com"
    
    # Execute
    # Should not raise KeyError
    rebuild_auth(mock_session, mock_prepared_request, mock_response)
    
    # Verify headers remain untouched
    assert "Authorization" not in mock_prepared_request.headers
    assert mock_prepared_request.headers["Content-Type"] == "application/json"