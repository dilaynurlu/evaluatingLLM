import pytest
from requests.sessions import Session
from requests.models import PreparedRequest, Response, Request

def test_rebuild_auth_keeps_header_on_same_host():
    """
    Test that Authorization headers are PRESERVED when redirecting to the same host
    (assuming trust_env is False to avoid netrc side effects interfering).
    """
    session = Session()
    session.trust_env = False  # Disable netrc logic to strictly test the retention logic
    
    # Original request context (Same Host)
    orig_req = Request('GET', 'http://example.com/path1')
    response = Response()
    response.request = orig_req.prepare()
    
    # New request context (Same Host, different path)
    new_req = PreparedRequest()
    new_req.prepare(
        method='GET', 
        url='http://example.com/path2',
        headers={'Authorization': 'Basic existing-token'}
    )
    
    session.rebuild_auth(new_req, response)
    
    # 'Authorization' should be present because the host is the same
    assert 'Authorization' in new_req.headers
    assert new_req.headers['Authorization'] == 'Basic existing-token'