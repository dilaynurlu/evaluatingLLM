import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.structures import CaseInsensitiveDict

def test_rebuild_auth_strips_authorization_on_https_to_http_downgrade():
    """
    Refined test to ensure authorization is stripped during a protocol downgrade (HTTPS -> HTTP),
    handling headers in a case-insensitive manner.
    """
    # Target function access
    rebuild_auth = Session.rebuild_auth
    
    # Setup mocks
    mock_session = MagicMock(spec=Session)
    mock_session.trust_env = False
    # Mocking should_strip_auth to True implies the session logic detected a downgrade or cross-origin
    mock_session.should_strip_auth.return_value = True
    
    mock_prepared_request = MagicMock()
    # Use CaseInsensitiveDict to mimic real Request behavior and test case-insensitivity
    # Using lowercase "authorization" key to verify strict lookup isn't used
    mock_prepared_request.headers = CaseInsensitiveDict({"authorization": "Basic sensitive_token"})
    
    # Simulate HTTPS -> HTTP downgrade
    mock_prepared_request.url = "http://insecure-host.com/resource"
    mock_response = MagicMock()
    mock_response.request.url = "https://secure-host.com/resource"
    
    # Execute
    rebuild_auth(mock_session, mock_prepared_request, mock_response)
    
    # Verify
    # The header should be removed regardless of casing
    assert "Authorization" not in mock_prepared_request.headers
    assert "authorization" not in mock_prepared_request.headers
    
    mock_session.should_strip_auth.assert_called_once_with(
        "https://secure-host.com/resource", "http://insecure-host.com/resource"
    )