import pytest
from unittest.mock import patch
import requests
from requests.models import Response, PreparedRequest

def test_resolve_redirects_fragment_handling():
    """
    Test that URL fragments are handled correctly:
    1. If new location has no fragment, inherit from original.
    2. If new location has fragment, use it.
    """
    session = requests.Session()
    
    # Scenario 1: Original has fragment, redirect has none -> Inherit
    req = PreparedRequest()
    req.prepare(method='GET', url='http://example.com/page#original-frag')
    
    resp = Response()
    resp.status_code = 302
    resp.headers['Location'] = '/newpage'
    resp.url = 'http://example.com/page'
    resp.request = req
    resp._content = b''
    
    with patch.object(session, 'send', return_value=Response()) as mock_send:
        gen = session.resolve_redirects(resp, req)
        next(gen, None)
        
        sent_req = mock_send.call_args[0][0]
        assert sent_req.url == 'http://example.com/newpage#original-frag'

    # Scenario 2: Redirect has new fragment -> Update
    # We must reset for a new clean test pass or just use a new call
    
    resp.headers['Location'] = '/newpage#new-frag'
    with patch.object(session, 'send', return_value=Response()) as mock_send:
        gen = session.resolve_redirects(resp, req)
        next(gen, None)
        
        sent_req = mock_send.call_args[0][0]
        assert sent_req.url == 'http://example.com/newpage#new-frag'