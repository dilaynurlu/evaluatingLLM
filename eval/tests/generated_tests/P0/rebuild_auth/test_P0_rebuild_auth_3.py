import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_applies_netrc_credentials_if_env_trusted():
    # Scenario: Redirect to a URL that has credentials in .netrc, and trust_env is True.
    # Expected: prepare_auth should be called with the new credentials.

    session = Session()
    session.trust_env = True
    session.should_strip_auth = MagicMock(return_value=False)

    # Setup Request without auth initially
    target_url = 'http://netrc-protected.com/resource'
    req = Request(method='GET', url=target_url)
    prepared_request = req.prepare()

    response = MagicMock(spec=Response)
    response.request = MagicMock()
    response.request.url = 'http://other.com'

    # Mock get_netrc_auth to return credentials
    fake_netrc_auth = ('user', 'pass')
    
    # We also spy on prepared_request.prepare_auth to verify it gets called
    with patch('requests.sessions.get_netrc_auth', return_value=fake_netrc_auth) as mock_get_netrc:
        with patch.object(prepared_request, 'prepare_auth', wraps=prepared_request.prepare_auth) as mock_prepare_auth:
            
            # Execute
            session.rebuild_auth(prepared_request, response)

            # Assert
            mock_get_netrc.assert_called_once_with(target_url)
            mock_prepare_auth.assert_called_once_with(fake_netrc_auth)
            
            # Since we allowed the real prepare_auth to run (wraps), header should be updated
            # (Note: requests transforms tuple auth to Basic Auth header)
            assert 'Authorization' in prepared_request.headers