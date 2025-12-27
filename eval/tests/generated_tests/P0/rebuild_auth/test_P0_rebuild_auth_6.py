import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_handles_missing_header_with_should_strip_true():
    # Scenario: should_strip_auth returns True, but request has no Authorization header.
    # Expected: No errors (KeyError), request remains unchanged.

    session = Session()
    session.should_strip_auth = MagicMock(return_value=True)
    session.trust_env = False

    # Request without Authorization
    req = Request(method='GET', url='http://new.com', headers={'Content-Type': 'application/json'})
    prepared_request = req.prepare()

    response = MagicMock(spec=Response)
    response.request = MagicMock()
    response.request.url = 'http://old.com'

    # Execute
    session.rebuild_auth(prepared_request, response)

    # Assert
    assert 'Authorization' not in prepared_request.headers
    assert prepared_request.headers['Content-Type'] == 'application/json'