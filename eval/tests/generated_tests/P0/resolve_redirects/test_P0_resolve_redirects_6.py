import pytest
from unittest.mock import Mock, MagicMock
from requests.sessions import Session
from requests.models import Response, Request, PreparedRequest

def test_resolve_redirects_yield_requests_true():
    """
    Test that setting yield_requests=True causes the generator to yield
    PreparedRequest objects instead of sending them and yielding responses.
    """
    session = Session()
    
    req = Request('GET', 'http://example.com/start')
    prep_req = session.prepare_request(req)
    
    resp = Response()
    resp.status_code = 302
    resp.headers['Location'] = 'http://example.com/next'
    resp.url = 'http://example.com/start'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Ensure session.send is NOT called
    session.send = Mock()
    
    gen = session.resolve_redirects(resp, prep_req, yield_requests=True)
    
    # The generator should yield the PreparedRequest for the next step
    yielded_obj = next(gen)
    
    assert isinstance(yielded_obj, PreparedRequest)
    assert yielded_obj.url == 'http://example.com/next'
    assert yielded_obj.method == 'GET'
    
    # session.send should not have been used
    session.send.assert_not_called()