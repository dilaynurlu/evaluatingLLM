import pytest
from unittest.mock import MagicMock
from requests import Session, Request, Response, PreparedRequest
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_yield_requests_true():
    """
    Test that when yield_requests=True is passed, the generator yields
    PreparedRequest objects instead of sending them and yielding responses.
    """
    session = Session()
    
    req = Request('GET', 'http://example.com/start').prepare()
    
    resp = Response()
    resp.status_code = 302
    resp.url = 'http://example.com/start'
    resp.headers = CaseInsensitiveDict({'Location': 'http://example.com/next'})
    resp.raw = MagicMock()
    
    # We set yield_requests=True, so session.send should NOT be called
    session.send = MagicMock()
    
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    yielded_obj = next(gen)
    
    # Assert we got a PreparedRequest
    assert isinstance(yielded_obj, PreparedRequest)
    assert yielded_obj.url == 'http://example.com/next'
    assert yielded_obj.method == 'GET'
    
    # Verify session.send was NOT called
    session.send.assert_not_called()