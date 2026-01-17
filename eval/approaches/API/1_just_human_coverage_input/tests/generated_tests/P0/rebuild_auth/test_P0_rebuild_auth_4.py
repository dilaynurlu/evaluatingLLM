import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_ignores_netrc_when_environment_untrusted():
    session = Session()
    # Explicitly disable environment trust
    session.trust_env = False
    
    req = PreparedRequest()
    req.prepare(
        method='GET',
        url='https://example.com/resource'
    )
    
    resp = Response()
    resp.request = PreparedRequest()
    resp.request.url = 'https://prev.com'
    
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        # Mocking return value to ensure it's NOT used
        mock_netrc.return_value = ('user', 'pass')
        
        session.rebuild_auth(req, resp)
        
        # Verify get_netrc_auth was never called due to trust_env check
        mock_netrc.assert_not_called()
        assert 'Authorization' not in req.headers