import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_preserves_authorization_when_stripping_not_required():
    """
    Refined test using CaseInsensitiveDict to ensure existing headers are preserved
    when the destination is safe.
    """
    # Target function access
    rebuild_auth = Session.rebuild_auth
    
    # Setup mocks
    mock_session = MagicMock(spec=Session)
    mock_session.trust_env = False
    mock_session.should_strip_auth.return_value = False
    
    mock_prepared_request = MagicMock()
    original_token = "Basic safe_token"
    # Use CaseInsensitiveDict
    mock_prepared_request.headers = CaseInsensitiveDict({"Authorization": original_token})
    mock_prepared_request.url = "https://same-host.com/new_path"
    
    mock_response = MagicMock()
    mock_response.request.url = "https://same-host.com/old_path"
    
    # Execute
    rebuild_auth(mock_session, mock_prepared_request, mock_response)
    
    # Verify
    assert "Authorization" in mock_prepared_request.headers
    assert mock_prepared_request.headers["Authorization"] == original_token