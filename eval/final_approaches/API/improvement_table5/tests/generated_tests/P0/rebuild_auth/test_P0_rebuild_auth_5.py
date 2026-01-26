import pytest
from unittest.mock import patch
from requests.sessions import Session
from requests.models import PreparedRequest, Response, Request
import base64

def test_rebuild_auth_strips_old_auth_and_applies_new_netrc():
    """
    Test scenario where redirect changes host:
    1. Old Authorization header should be stripped.
    2. New Authorization header from .netrc should be applied.
    """
    session = Session()
    session.trust_env = True
    
    # Redirect from Host A -> Host B
    orig_req = Request('GET', 'http://host-a.com/')
    response = Response()
    response.request = orig_req.prepare()
    
    # Request prepared with old auth headers (copied from original)
    new_req = PreparedRequest()
    new_req.prepare(
        method='GET', 
        url='http://host-b.com/',
        headers={'Authorization': 'Basic old-host-credentials'}
    )
    
    # Netrc has credentials for Host B
    new_creds = ('newuser', 'newpass')
    with patch('requests.sessions.get_netrc_auth', return_value=new_creds):
        session.rebuild_auth(new_req, response)
    
    expected_b64 = base64.b64encode(b"newuser:newpass").decode('ascii')
    expected_header = f"Basic {expected_b64}"
    
    # The header should now be the new credentials
    assert new_req.headers['Authorization'] == expected_header
    # Sanity check: ensure we didn't just append or mess up
    assert 'old-host-credentials' not in new_req.headers['Authorization']