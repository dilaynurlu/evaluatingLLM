import pytest
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_strips_header_on_redirect_host_change():
    """
    Test that Authorization header is removed when redirecting to a different host
    and trust_env is False (so no new netrc auth is applied).
    """
    session = Session()
    session.trust_env = False
    
    # Setup original request and response (Source)
    orig_url = "http://example.com/login"
    response = Response()
    response.request = Request(method='POST', url=orig_url).prepare()
    
    # Setup new request to a different host (Destination)
    new_url = "http://other-host.com/dashboard"
    headers = {'Authorization': 'Basic c2VjcmV0OnBhc3M=', 'Accept': 'application/json'}
    new_request = Request(method='GET', url=new_url, headers=headers).prepare()
    
    # Pre-condition check
    assert 'Authorization' in new_request.headers
    
    # Execute
    session.rebuild_auth(new_request, response)
    
    # Verify Authorization is removed, other headers remain
    assert 'Authorization' not in new_request.headers
    assert new_request.headers['Accept'] == 'application/json'