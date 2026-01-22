import pytest
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest
from unittest.mock import Mock

def test_resolve_redirects_yield_requests():
    """
    Test that setting yield_requests=True causes the generator to yield
    the PreparedRequest object instead of sending it and yielding a Response.
    """
    session = Session()
    session.max_redirects = 5
    
    req = Request('GET', 'http://example.com/start').prepare()
    
    resp1 = Response()
    resp1.status_code = 301
    resp1.headers['Location'] = '/next'
    resp1.url = 'http://example.com/start'
    resp1._content = b""
    resp1.raw = Mock()
    resp1.request = req
    
    # We mock send just in case, but it should NOT be called if we yield requests.
    session.send = Mock()
    
    gen = session.resolve_redirects(resp1, req, yield_requests=True)
    
    # Get the first yielded item
    item = next(gen)
    
    # It should be a PreparedRequest object
    assert isinstance(item, PreparedRequest)
    assert item.url == 'http://example.com/next'
    
    # session.send should not have been called yet because yielding request pauses execution
    assert session.send.call_count == 0
    
    # Close generator to cleanup
    gen.close()