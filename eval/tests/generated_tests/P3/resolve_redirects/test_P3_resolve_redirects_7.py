import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest

def test_resolve_redirects_yield_requests_true():
    """
    Test the yield_requests=True parameter.
    Verify that resolve_redirects yields the PreparedRequest object 
    for the redirect instead of performing the request and yielding a Response.
    """
    session = Session()
    
    req = Request('GET', 'http://example.com/start')
    prep_req = session.prepare_request(req)
    
    resp = Response()
    resp.status_code = 301
    resp.url = 'http://example.com/start'
    resp.headers['Location'] = 'http://example.com/stop'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # We do NOT mock send() because it should not be called when yield_requests=True
    session.send = MagicMock()
    
    gen = session.resolve_redirects(resp, prep_req, yield_requests=True)
    
    # Get the first yield
    yielded_obj = next(gen)
    
    # It should be a PreparedRequest
    assert isinstance(yielded_obj, PreparedRequest)
    assert yielded_obj.url == 'http://example.com/stop'
    
    # Verify send was not called
    session.send.assert_not_called()