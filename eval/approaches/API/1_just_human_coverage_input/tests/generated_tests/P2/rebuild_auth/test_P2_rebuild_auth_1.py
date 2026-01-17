import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_strips_credentials_on_cross_domain_redirect():
    """
    Test that Authorization headers are removed when redirecting to a location
    that requires auth stripping (e.g. cross-origin), and no new auth is available from netrc.
    """
    # Create a session and configure it to strip auth
    session = Session()
    # Mock should_strip_auth to force True, simulating a cross-origin redirect
    session.should_strip_auth = Mock(return_value=True)
    # Disable trust_env to prevent netrc lookup logic from interfering
    session.trust_env = False

    # Create a PreparedRequest with an existing Authorization header
    # We use Request(...).prepare() to ensure the object is correctly initialized
    original_auth = ("user", "pass")
    prepared_request = Request(
        "GET", 
        "https://new-host.com/resource", 
        auth=original_auth
    ).prepare()
    
    # Verify preconditions: Authorization header exists
    assert "Authorization" in prepared_request.headers
    
    # Create the response that triggered the redirect
    response = Response()
    # Attach the original request to the response
    response.request = Request("GET", "https://old-host.com/resource").prepare()

    # Call the target function
    session.rebuild_auth(prepared_request, response)

    # Assertions
    # The Authorization header should be removed
    assert "Authorization" not in prepared_request.headers
    
    # Verify should_strip_auth was called with expected URLs
    session.should_strip_auth.assert_called_once_with(
        "https://old-host.com/resource", 
        "https://new-host.com/resource"
    )