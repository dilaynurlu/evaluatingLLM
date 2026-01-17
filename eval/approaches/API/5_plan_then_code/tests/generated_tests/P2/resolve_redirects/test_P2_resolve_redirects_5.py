import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_fragment_persistence():
    """
    Test that URL fragments are handled correctly during redirects:
    1. If new URL has no fragment, the original fragment is preserved.
    2. If new URL has a fragment, it overrides the original.
    
    This test focuses on case 1: Original fragment preservation.
    """
    session = Session()
    
    # Initial URL has a fragment
    fragment = '#section1'
    initial_url = 'http://example.com/start' + fragment
    target_url_base = 'http://example.com/middle'
    
    req = Request('GET', initial_url).prepare()
    
    resp = Response()
    resp.status_code = 302
    resp.url = initial_url
    # Location header lacks fragment
    resp.headers['Location'] = target_url_base
    resp._content = b''
    resp._content_consumed = True
    resp.request = req
    
    captured_requests = []
    def side_effect(request, **kwargs):
        captured_requests.append(request)
        r = Response()
        r.status_code = 200
        r.url = request.url
        r._content = b'OK'
        r._content_consumed = True
        return r
        
    session.send = Mock(side_effect=side_effect)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    sent_req = captured_requests[0]
    
    # Verify fragment was appended to the new URL
    assert sent_req.url == target_url_base + fragment