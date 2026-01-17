import pytest
from unittest.mock import patch, Mock
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_strips_old_credentials_and_applies_new_netrc_auth():
    session = Session()
    session.trust_env = True
    # Force stripping of the old auth header
    session.should_strip_auth = Mock(return_value=True)
    
    req = PreparedRequest()
    req.prepare(
        method='GET',
        url='https://new-host.com/secure',
        headers={'Authorization': 'Bearer old-compromised-token'}
    )
    
    resp = Response()
    old_req = PreparedRequest()
    old_req.prepare(method='GET', url='https://old-host.com/secure')
    resp.request = old_req
    
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        # Provide new credentials for the new host
        mock_netrc.return_value = ('newuser', 'newpass')
        
        session.rebuild_auth(req, resp)
        
        # Verify interactions
        session.should_strip_auth.assert_called_once()
        mock_netrc.assert_called_once_with('https://new-host.com/secure')
        
        # Verify the Authorization header was updated
        assert 'Authorization' in req.headers
        auth_val = req.headers['Authorization']
        # Should be Basic auth now, not the old Bearer
        assert auth_val.startswith('Basic ')
        assert 'Bearer' not in auth_val