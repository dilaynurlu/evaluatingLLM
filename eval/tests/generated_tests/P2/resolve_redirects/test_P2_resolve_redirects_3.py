import pytest
from unittest.mock import patch
import requests
from requests.models import Response, PreparedRequest

def test_resolve_redirects_303_convert_to_get():
    """
    Test that a 303 See Other redirect converts the method to GET
    and removes body-specific headers (Content-Length, Content-Type).
    """
    session = requests.Session()
    
    # Original POST request
    req = PreparedRequest()
    req.prepare(
        method='POST',
        url='http://example.com/submit',
        headers={'Content-Type': 'application/json', 'Content-Length': '15'},
        data='{"data": true}'
    )
    
    # Response triggering 303 redirect
    resp = Response()
    resp.status_code = 303
    resp.headers['Location'] = '/success'
    resp.url = 'http://example.com/submit'
    resp.request = req
    resp._content = b''
    
    # Target response
    target_resp = Response()
    target_resp.status_code = 200
    target_resp.url = 'http://example.com/success'
    target_resp._content = b'OK'
    
    with patch.object(session, 'send', return_value=target_resp) as mock_send:
        gen = session.resolve_redirects(resp, req)
        next(gen)
        
        # Inspect the request that was sent via session.send
        call_args = mock_send.call_args
        sent_req = call_args[0][0]
        
        assert sent_req.method == 'GET'
        assert sent_req.url == 'http://example.com/success'
        assert sent_req.body is None
        assert 'Content-Type' not in sent_req.headers
        assert 'Content-Length' not in sent_req.headers