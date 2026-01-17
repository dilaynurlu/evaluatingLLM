import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_retains_credentials_on_safe_redirect():
    """
    Test that Authorization headers are retained when redirecting to a location
    where stripping is NOT required (e.g. same origin).
    """
    # Create a session
    session = Session()
    # Mock should_strip_auth to force False (safe redirect)
    session.should_strip_auth = Mock(return_value=False)
    session.trust_env = False

    # Create a PreparedRequest with Authorization
    original_auth = ("user", "pass")
    prepared_request = Request(
        "GET", 
        "https://same-host.com/new-path", 
        auth=original_auth
    ).prepare()
    
    # Capture the original header value
    original_header_val = prepared_request.headers["Authorization"]
    
    # Create response context
    response = Response()
    response.request = Request("GET", "https://same-host.com/old-path").prepare()

    # Call target function
    session.rebuild_auth(prepared_request, response)

    # Assertions
    # Auth should still be present and unchanged
    assert "Authorization" in prepared_request.headers
    assert prepared_request.headers["Authorization"] == original_header_val
    
    session.should_strip_auth.assert_called_once()