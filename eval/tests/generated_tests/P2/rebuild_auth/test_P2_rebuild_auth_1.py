import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session

def test_rebuild_auth_strips_authorization_on_redirect():
    """
    Test that the 'Authorization' header is removed from the prepared request
    when should_strip_auth returns True (e.g., redirecting to a less secure or different host).
    """
    session = Session()
    
    # Force should_strip_auth to True to simulate a scenario where auth stripping is required
    session.should_strip_auth = Mock(return_value=True)
    # Ensure environment is not trusted to isolate the stripping logic from netrc logic
    session.trust_env = False

    # Setup the PreparedRequest with an existing Authorization header
    prepared_request = Mock()
    prepared_request.headers = {"Authorization": "Basic dXNlcjpwYXNz"}
    prepared_request.url = "http://example-new.com/resource"

    # Setup the Response that triggered the redirect
    response = Mock()
    response.request.url = "http://example-old.com/resource"

    # Patch get_netrc_auth to ensure no side effects (though trust_env=False handles this)
    with patch("requests.sessions.get_netrc_auth") as mock_netrc:
        session.rebuild_auth(prepared_request, response)

    # Verify Authorization header was removed
    assert "Authorization" not in prepared_request.headers
    
    # Verify should_strip_auth was called with correct URLs
    session.should_strip_auth.assert_called_once_with(
        "http://example-old.com/resource", 
        "http://example-new.com/resource"
    )