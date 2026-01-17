import pytest
from unittest.mock import patch, Mock
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_applies_netrc_credentials_when_environment_trusted():
    session = Session()
    # Enable environment trust to allow netrc lookup
    session.trust_env = True
    # should_strip_auth logic is irrelevant here as there is no initial auth header
    session.should_strip_auth = Mock(return_value=False)
    
    target_url = 'https://authenticated.com/data'
    req = PreparedRequest()
    req.prepare(
        method='GET',
        url=target_url
        # No initial headers
    )
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = 'https://original.com'
    
    # Mock get_netrc_auth to return valid credentials
    # We patch it in requests.sessions because that is where rebuild_auth looks it up
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        mock_netrc.return_value = ('testuser', 'testpass')
        
        session.rebuild_auth(req, resp)
        
        mock_netrc.assert_called_once_with(target_url)
        assert 'Authorization' in req.headers
        # When a tuple is returned, requests applies HTTPBasicAuth
        assert req.headers['Authorization'].startswith('Basic ')