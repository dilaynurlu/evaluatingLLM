import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_preserves_authorization_when_redirecting_to_trusted_host():
    session = Session()
    session.trust_env = False
    
    # Simulate a redirect where auth should NOT be stripped (e.g. same domain)
    session.should_strip_auth = Mock(return_value=False)
    
    # Create a request with an Authorization header
    req = PreparedRequest()
    req.prepare(
        method='GET',
        url='https://api.example.com/v2/resource',
        headers={'Authorization': 'Bearer my-token'}
    )
    
    # Create a response object
    resp = Response()
    old_req = PreparedRequest()
    old_req.prepare(method='GET', url='https://api.example.com/v1/resource')
    resp.request = old_req
    
    # Execute
    session.rebuild_auth(req, resp)
    
    # Assertions
    assert 'Authorization' in req.headers
    assert req.headers['Authorization'] == 'Bearer my-token'
    session.should_strip_auth.assert_called_once()