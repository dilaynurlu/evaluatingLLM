import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_ignores_netrc_if_env_untrusted():
    # Scenario: .netrc has credentials, but session.trust_env is False.
    # Expected: No new authentication should be applied.

    session = Session()
    session.trust_env = False
    
    req = Request(method='GET', url='http://netrc-protected.com/resource')
    prepared_request = req.prepare()

    response = MagicMock(spec=Response)
    response.request = MagicMock()
    response.request.url = 'http://other.com'

    # Even if get_netrc_auth were to return credentials, it shouldn't affect the request
    # We patch it just to ensure logic doesn't call it or ignores it depending on implementation
    # The implementation checks trust_env first, but if it checked after, we verify outcome.
    with patch('requests.sessions.get_netrc_auth', return_value=('user', 'pass')) as mock_get_netrc:
        with patch.object(prepared_request, 'prepare_auth') as mock_prepare_auth:
            
            # Execute
            session.rebuild_auth(prepared_request, response)

            # Assert
            # Since trust_env is False, get_netrc_auth should strictly not be called 
            # based on "if self.trust_env" check in the source.
            mock_get_netrc.assert_not_called()
            mock_prepare_auth.assert_not_called()

'''
Manually marked in csv as assertion correct. Because it has assertions, just not recongnized by the tool.
''' 