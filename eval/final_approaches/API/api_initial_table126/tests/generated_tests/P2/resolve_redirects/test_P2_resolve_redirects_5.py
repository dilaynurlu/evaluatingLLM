import pytest
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest

def test_resolve_redirects_maintains_fragment():
    """
    Test that the URL fragment is maintained during redirect if the new Location
    does not specify one.
    """
    session = Session()
    
    # Initial request with fragment
    original_url = 'http://example.com/page#section1'
    req = Request('GET', original_url).prepare()
    
    # 302 Response with Location having NO fragment
    resp = Response()
    resp.status_code = 302
    resp.headers['Location'] = '/newpage'  # Relative path, no fragment
    resp.url = original_url
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    
    # Execute with yield_requests=True
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    new_req = next(gen)
    
    # Expect full URL with original fragment
    assert new_req.url == 'http://example.com/newpage#section1'

    # Now test case where Location HAS a fragment
    resp.headers['Location'] = '/newpage#section2'
    gen2 = session.resolve_redirects(resp, req, yield_requests=True)
    new_req2 = next(gen2)
    
    # Expect new fragment to override
    assert new_req2.url == 'http://example.com/newpage#section2'