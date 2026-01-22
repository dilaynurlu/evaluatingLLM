import pytest
from requests.sessions import Session
from requests.models import Request, Response
from unittest.mock import Mock

def test_resolve_redirects_fragment_handling():
    """
    Test handling of URL fragments during redirect.
    - If new Location has no fragment, the original fragment should be preserved (RFC 7231).
    - If new Location has a fragment, it should be used.
    """
    session = Session()
    session.max_redirects = 5
    
    # Case 1: Original has fragment, Location does not.
    # Original: http://example.com/old#frag
    # Location: http://example.com/new
    # Expected: http://example.com/new#frag
    
    req = Request('GET', 'http://example.com/old', headers={}).prepare()
    # Manually attach fragment to prepared request url if not handled by prepare?
    # Request prepare handles it.
    req.url = 'http://example.com/old#frag' 
    
    resp1 = Response()
    resp1.status_code = 301
    resp1.headers['Location'] = '/new'
    resp1.url = 'http://example.com/old'
    resp1._content = b""
    resp1.raw = Mock()
    resp1.request = req
    
    resp2 = Response()
    resp2.status_code = 200
    resp2.url = 'http://example.com/new#frag'
    resp2._content = b"OK"
    resp2.raw = Mock()
    
    session.send = Mock(return_value=resp2)
    
    list(session.resolve_redirects(resp1, req))
    
    args, _ = session.send.call_args
    sent_req = args[0]
    
    assert sent_req.url == 'http://example.com/new#frag'