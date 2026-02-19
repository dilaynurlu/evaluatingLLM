import pytest
from unittest.mock import Mock, patch
import requests

def test_resolve_redirects_yield_requests():
    """
    Test that if yield_requests is True, the generator yields PreparedRequest objects
    instead of sending them and yielding responses.
    """
    session = requests.Session()
    
    initial_req = requests.Request('GET', 'http://example.com/start').prepare()
    
    initial_resp = requests.Response()
    initial_resp.status_code = 302
    initial_resp.headers['Location'] = '/next'
    initial_resp.url = 'http://example.com/start'
    initial_resp.request = initial_req
    initial_resp._content = b''
    initial_resp._content_consumed = True
    initial_resp.raw = Mock()

    # Call with yield_requests=True
    gen = session.resolve_redirects(initial_resp, initial_req, yield_requests=True)
    
    # Expect a PreparedRequest object
    item = next(gen)
    assert isinstance(item, requests.PreparedRequest)
    assert item.url == 'http://example.com/next'
    
    # Since we are not running the full loop (which would require updating 'url' or 'resp' logic 
    # to avoid infinite loop on same response), we check the first yield.