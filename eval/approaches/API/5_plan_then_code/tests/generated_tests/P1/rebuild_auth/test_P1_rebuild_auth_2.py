import pytest
from requests.sessions import Session
from requests.models import Request, Response

def test_rebuild_auth_preserves_header_on_same_host_redirect():
    """
    Test that Authorization header is preserved when redirecting to the same host.
    """
    session = Session()
    session.trust_env = False
    
    # Setup original request and response (Source)
    orig_url = "http://example.com/page1"
    response = Response()
    response.request = Request(method='GET', url=orig_url).prepare()
    
    # Setup new request to the same host (Destination)
    new_url = "http://example.com/page2"
    auth_val = 'Basic c2VjcmV0OnBhc3M='
    headers = {'Authorization': auth_val}
    new_request = Request(method='GET', url=new_url, headers=headers).prepare()
    
    # Execute
    session.rebuild_auth(new_request, response)
    
    # Verify Authorization is preserved
    assert 'Authorization' in new_request.headers
    assert new_request.headers['Authorization'] == auth_val