import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_retains_authorization_safe_redirect():
    """
    Test that the 'Authorization' header is preserved in the prepared request
    when should_strip_auth returns False (e.g., redirecting to the same host).
    """
    session = Session()
    
    # Force should_strip_auth to False to simulate a safe redirect
    session.should_strip_auth = Mock(return_value=False)
    session.trust_env = False

    original_auth_header = "Basic dXNlcjpwYXNz"
    
    # Setup the PreparedRequest
    prepared_request = Mock()
    prepared_request.headers = {"Authorization": original_auth_header}
    prepared_request.url = "https://example.com/new_path"

    # Setup the Response
    response = Mock()
    response.request.url = "https://example.com/old_path"

    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        session.rebuild_auth(prepared_request, response)

    # Verify Authorization header remains unchanged
    assert prepared_request.headers.get("Authorization") == original_auth_header
    
    session.should_strip_auth.assert_called_once()