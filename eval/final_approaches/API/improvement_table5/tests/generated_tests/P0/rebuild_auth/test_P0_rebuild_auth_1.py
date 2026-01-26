import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response, Request

def test_rebuild_auth_strips_header_on_different_host():
    """
    Test that Authorization headers are stripped when redirecting to a different host,
    and no new Netrc credentials are applied (simulated by returning None).
    """
    session = Session()
    session.trust_env = True  # Enable checking netrc, to verify we try but find nothing
    
    # Original request context (Host A)
    orig_req = Request('GET', 'http://host-a.com/sensitive-data')
    response = Response()
    response.request = orig_req.prepare()
    
    # New request context (Host B)
    # The RedirectMixin typically copies headers to the new request before calling rebuild_auth
    new_req = PreparedRequest()
    new_req.prepare(
        method='GET', 
        url='http://host-b.com/other',
        headers={'Authorization': 'Basic oldsecret', 'User-Agent': 'my-app'}
    )
    
    # Patch get_netrc_auth to return None, simulating no entry in .netrc for host-b.com
    with patch('requests.sessions.get_netrc_auth', return_value=None):
        session.rebuild_auth(new_req, response)
        
    # 'Authorization' should be removed because host changed
    assert 'Authorization' not in new_req.headers
    # Other headers should remain untouched
    assert new_req.headers['User-Agent'] == 'my-app'