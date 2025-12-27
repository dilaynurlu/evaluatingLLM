import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_strips_authorization_on_unsafe_redirect():
    # Scenario: Redirecting to a different host (unsafe).
    # Expected: The 'Authorization' header should be removed from the prepared request.

    # Setup Session
    session = Session()
    # Mock should_strip_auth to force True, simulating an unsafe redirect decision
    session.should_strip_auth = MagicMock(return_value=True)
    # Disable trust_env to ensure we don't accidentally pick up netrc credentials in this test
    session.trust_env = False

    # Setup PreparedRequest using public API
    # We include an Authorization header initially
    req = Request(
        method='GET',
        url='http://new-malicious-host.com/path',
        headers={'Authorization': 'Basic c2VjcmV0OnBhc3N3b3Jk'}
    )
    prepared_request = req.prepare()

    # Verify setup precondition
    assert 'Authorization' in prepared_request.headers

    # Setup Response Mock (we only need the request URL from the previous response)
    response = MagicMock(spec=Response)
    response.request = MagicMock()
    response.request.url = 'http://original-safe-host.com/path'

    # Execute target function
    session.rebuild_auth(prepared_request, response)

    # Assert
    # The Authorization header must be gone
    assert 'Authorization' not in prepared_request.headers
    
    # Verify interaction
    session.should_strip_auth.assert_called_once_with(
        'http://original-safe-host.com/path',
        'http://new-malicious-host.com/path'
    )