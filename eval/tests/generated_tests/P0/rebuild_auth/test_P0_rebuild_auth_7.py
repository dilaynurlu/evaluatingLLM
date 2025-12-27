import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_does_nothing_if_netrc_returns_none():
    # Scenario: trust_env is True, but get_netrc_auth returns None (no entry found).
    # Expected: prepare_auth is not called.

    session = Session()
    session.trust_env = True
    session.should_strip_auth = MagicMock(return_value=False)

    req = Request(method='GET', url='http://no-creds.com')
    prepared_request = req.prepare()

    response = MagicMock(spec=Response)
    response.request = MagicMock()
    response.request.url = 'http://old.com'

    with patch('requests.sessions.get_netrc_auth', return_value=None) as mock_get_netrc:
        with patch.object(prepared_request, 'prepare_auth') as mock_prepare_auth:
            
            # Execute
            session.rebuild_auth(prepared_request, response)

            # Assert
            mock_get_netrc.assert_called_once()
            mock_prepare_auth.assert_not_called()

'''
Manually marked in csv as assertion correct. Because it has assertions, just not recongnized by the tool.
'''