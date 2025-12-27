import pytest
from unittest.mock import patch
import requests
from requests.models import Response, PreparedRequest

def test_resolve_redirects_307_preserve_post():
    """
    Test that a 307 Temporary Redirect preserves the POST method
    and the request body/headers.
    """
    session = requests.Session()
    
    # Original POST request
    req = PreparedRequest()
    body_data = '{"data": "preserve me"}'
    req.prepare(
        method='POST',
        url='http://example.com/api/v1',
        headers={'Content-Type': 'application/json'},
        data=body_data
    )
    
    # Response triggering 307 redirect
    resp = Response()
    resp.status_code = 307
    resp.headers['Location'] = 'http://example.com/api/v2'
    resp.url = 'http://example.com/api/v1'
    resp.request = req
    resp._content = b''
    
    with patch.object(session, 'send', return_value=Response()) as mock_send:
        gen = session.resolve_redirects(resp, req)
        next(gen, None)
        
        sent_req = mock_send.call_args[0][0]
        
        assert sent_req.method == 'POST'
        assert sent_req.url == 'http://example.com/api/v2'
        assert sent_req.headers['Content-Type'] == 'application/json'
        assert sent_req.body == body_data