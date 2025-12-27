import pytest
from unittest.mock import patch
import requests
from requests.models import Response, PreparedRequest

def test_resolve_redirects_yield_requests():
    """
    Test that setting yield_requests=True causes the generator to yield
    PreparedRequest objects instead of following them automatically via send().
    """
    session = requests.Session()
    
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/start')
    
    resp = Response()
    resp.status_code = 301
    resp.headers['Location'] = 'http://example.com/moved'
    resp.url = 'http://example.com/start'
    resp.request = req
    resp._content = b''
    
    # We do NOT expect session.send to be called
    with patch.object(session, 'send') as mock_send:
        gen = session.resolve_redirects(resp, req, yield_requests=True)
        
        yielded_item = next(gen)
        
        # It should be a PreparedRequest
        assert isinstance(yielded_item, PreparedRequest)
        assert yielded_item.url == 'http://example.com/moved'
        assert yielded_item.method == 'GET'
        
        mock_send.assert_not_called()