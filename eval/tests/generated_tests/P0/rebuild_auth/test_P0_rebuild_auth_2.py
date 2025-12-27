import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_preserves_authorization_on_safe_redirect():
    # Scenario: Redirecting to a safe/trusted host (e.g. same domain).
    # Expected: The 'Authorization' header should remain in the prepared request.

    session = Session()
    # Mock should_strip_auth to return False
    session.should_strip_auth = MagicMock(return_value=False)
    session.trust_env = False

    # Setup PreparedRequest with Authorization
    original_auth = 'Basic c2VjcmV0OnBhc3N3b3Jk'
    req = Request(
        method='GET',
        url='http://same-host.com/new-path',
        headers={'Authorization': original_auth}
    )
    prepared_request = req.prepare()

    response = MagicMock(spec=Response)
    response.request = MagicMock()
    response.request.url = 'http://same-host.com/old-path'

    # Execute
    session.rebuild_auth(prepared_request, response)

    # Assert
    assert 'Authorization' in prepared_request.headers
    assert prepared_request.headers['Authorization'] == original_auth