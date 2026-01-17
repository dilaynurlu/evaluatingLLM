import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import Request, Response
from requests.auth import _basic_auth_str

def test_rebuild_auth_applies_netrc_credentials_if_trusted():
    """
    Test that new credentials from .netrc are applied to the request 
    if trust_env is True and credentials are found for the new host.
    """
    session = Session()
    session.trust_env = True
    
    # Setup original request (irrelevant host for this test, but needed for structure)
    response = Response()
    response.request = Request(method='GET', url="http://example.com").prepare()
    
    # Setup new request with no initial auth
    new_url = "http://internal.api/resource"
    new_request = Request(method='GET', url=new_url).prepare()
    
    user, pwd = "netrc_user", "netrc_pass"
    
    # Mock get_netrc_auth to return credentials for the new URL
    with patch('requests.sessions.get_netrc_auth', return_value=(user, pwd)) as mock_netrc:
        session.rebuild_auth(new_request, response)
        mock_netrc.assert_called_with(new_url)
    
    # Verify that the new credentials were applied as Basic Auth
    expected_auth = _basic_auth_str(user, pwd)
    assert 'Authorization' in new_request.headers
    assert new_request.headers['Authorization'] == expected_auth