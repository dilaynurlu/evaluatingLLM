import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response

@patch("requests.sessions.get_netrc_auth")
def test_rebuild_auth_applies_netrc_credentials_when_trusted_env(mock_get_netrc):
    """
    Test that credentials from .netrc are applied to the request when the
    environment is trusted and new credentials are found.
    """
    # Configure mock to return specific credentials
    netrc_auth = ("netrc_user", "netrc_pass")
    mock_get_netrc.return_value = netrc_auth

    session = Session()
    session.trust_env = True  # Enable netrc lookup
    session.should_strip_auth = Mock(return_value=False)

    # Create a request with NO existing auth
    prepared_request = Request("GET", "https://example.com/resource").prepare()
    assert "Authorization" not in prepared_request.headers

    # Create response context
    response = Response()
    response.request = Request("GET", "https://example.com/old").prepare()

    # Call target function
    session.rebuild_auth(prepared_request, response)

    # Assertions
    # prepare_auth should have been triggered by the netrc result.
    # Check if Authorization header is added. 
    # Basic auth for 'netrc_user:netrc_pass' should be present.
    assert "Authorization" in prepared_request.headers
    assert "Basic" in prepared_request.headers["Authorization"]
    
    # Verify netrc lookup used the new URL
    mock_get_netrc.assert_called_once_with("https://example.com/resource")