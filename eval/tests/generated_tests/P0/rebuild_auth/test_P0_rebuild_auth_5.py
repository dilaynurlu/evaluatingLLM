import pytest
from unittest.mock import MagicMock, patch
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_strips_old_and_applies_new_netrc_auth():
    # Scenario: Unsafe redirect (strip old auth) AND target has .netrc entry (apply new auth).
    # Expected: Old Authorization header removed, New Authorization header applied.

    session = Session()
    session.trust_env = True
    session.should_strip_auth = MagicMock(return_value=True)

    # Initial request has old credentials
    req = Request(
        method='GET', 
        url='http://new-host.com/resource',
        headers={'Authorization': 'Basic old_creds'}
    )
    prepared_request = req.prepare()

    response = MagicMock(spec=Response)
    response.request = MagicMock()
    response.request.url = 'http://old-host.com/resource'

    new_creds = ('new_user', 'new_pass')

    with patch('requests.sessions.get_netrc_auth', return_value=new_creds):
        # Execute
        session.rebuild_auth(prepared_request, response)

        # Assert
        # The logic is:
        # 1. Strip 'Authorization' if unsafe (it is).
        # 2. Get netrc auth.
        # 3. Apply netrc auth.
        
        # If prepare_auth works correctly, we should see new headers.
        # But we also implicitly verify the old one was stripped before applying new?
        # Actually, if the old one wasn't stripped, prepare_auth might overwrite it anyway.
        # To strictly verify stripping happened, we can check that should_strip_auth was consulted.
        # And physically, the headers will contain the NEW auth.
        
        assert 'Authorization' in prepared_request.headers
        # Verify it corresponds to the new credentials
        # Basic Auth for new_user:new_pass -> bmV3X3VzZXI6bmV3X3Bhc3M=
        assert prepared_request.headers['Authorization'] == 'Basic bmV3X3VzZXI6bmV3X3Bhc3M='
        
        session.should_strip_auth.assert_called_once()