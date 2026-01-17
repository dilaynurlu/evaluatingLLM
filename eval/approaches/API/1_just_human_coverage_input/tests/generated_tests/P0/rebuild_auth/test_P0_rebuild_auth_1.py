import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import PreparedRequest, Response

def test_rebuild_auth_strips_authorization_when_redirecting_to_new_host():
    session = Session()
    # Disable trust_env to focus purely on stripping logic (avoids netrc side effects)
    session.trust_env = False
    
    # Simulate a redirect where auth should be stripped (e.g. cross-domain)
    session.should_strip_auth = Mock(return_value=True)
    
    # Create a request with an Authorization header
    req = PreparedRequest()
    req.prepare(
        method='GET',
        url='https://new-secure.com/resource',
        headers={'Authorization': 'Bearer sensitive-token'}
    )
    
    # Create a response object representing the redirect source
    resp = Response()
    old_req = PreparedRequest()
    old_req.prepare(method='GET', url='https://old-insecure.com/resource')
    resp.request = old_req
    
    # Execute the target function
    session.rebuild_auth(req, resp)
    
    # Assertions
    assert 'Authorization' not in req.headers
    session.should_strip_auth.assert_called_once_with(
        'https://old-insecure.com/resource',
        'https://new-secure.com/resource'
    )