import pytest
from unittest.mock import Mock, MagicMock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_relative_url_and_fragment():
    """
    Test that relative redirect URLs are resolved correctly against the original URL,
    and that fragments are handled/persisted according to RFC rules.
    """
    session = Session()
    
    # Initial request with a fragment
    req = Request('GET', 'http://example.com/folder/page?q=1#section1')
    prep_req = session.prepare_request(req)
    
    # Response 301 with relative Location and NO fragment
    resp = Response()
    resp.status_code = 301
    resp.headers['Location'] = '../other'
    resp.url = 'http://example.com/folder/page?q=1'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Next response
    resp_next = Response()
    resp_next.status_code = 200
    resp_next.raw = MagicMock()
    
    session.send = Mock(return_value=resp_next)
    
    gen = session.resolve_redirects(resp, prep_req)
    next(gen)
    
    sent_req = session.send.call_args[0][0]
    
    # URL resolution:
    # Base: http://example.com/folder/page
    # Relative: ../other
    # Result: http://example.com/other
    # Fragment: Should be inherited from original request if missing in location
    
    assert sent_req.url == 'http://example.com/other#section1'
    
    # Test case 2: Location has a fragment, it should override
    # We create a new sequence for the second part of this test
    
    req2 = Request('GET', 'http://example.com/foo#old')
    prep_req2 = session.prepare_request(req2)
    
    resp2 = Response()
    resp2.status_code = 301
    resp2.headers['Location'] = '/bar#new'
    resp2.url = 'http://example.com/foo'
    resp2.request = prep_req2
    resp2._content = b""
    resp2._content_consumed = True
    resp2.raw = MagicMock()
    
    session.send = Mock(return_value=resp_next)
    
    gen2 = session.resolve_redirects(resp2, prep_req2)
    next(gen2)
    
    sent_req2 = session.send.call_args[0][0]
    assert sent_req2.url == 'http://example.com/bar#new'