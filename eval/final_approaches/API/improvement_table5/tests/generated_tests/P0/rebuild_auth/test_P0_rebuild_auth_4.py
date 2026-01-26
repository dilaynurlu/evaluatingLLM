import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response, Request

def test_rebuild_auth_ignores_netrc_if_untrusted_env():
    """
    Test that .netrc lookup is skipped if session.trust_env is False.
    """
    session = Session()
    session.trust_env = False
    
    orig_req = Request('GET', 'http://public.com/')
    response = Response()
    response.request = orig_req.prepare()
    
    new_req = PreparedRequest()
    new_req.prepare(method='GET', url='http://protected.com/')
    
    # Patch get_netrc_auth; if logic is correct, this should NOT be called
    with patch('requests.sessions.get_netrc_auth') as mock_netrc:
        # We can make it return something, but it shouldn't matter
        mock_netrc.return_value = ('user', 'pass')
        
        session.rebuild_auth(new_req, response)
        
        mock_netrc.assert_not_called()
        
    assert 'Authorization' not in new_req.headers