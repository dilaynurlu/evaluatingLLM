import pytest
from unittest.mock import Mock, patch
import requests

def test_resolve_redirects_303_downgrades_to_get():
    """
    Test that a 303 See Other redirect changes POST to GET and removes body-related headers.
    """
    session = requests.Session()
    
    initial_req = requests.Request(
        'POST', 
        'http://example.com/post', 
        data='test_data',
        headers={'Content-Type': 'text/plain', 'Content-Length': '9'}
    ).prepare()
    
    initial_resp = requests.Response()
    initial_resp.status_code = 303
    initial_resp.headers['Location'] = '/target'
    initial_resp.url = 'http://example.com/post'
    initial_resp.request = initial_req
    initial_resp._content = b''
    initial_resp._content_consumed = True
    initial_resp.raw = Mock()

    def send_side_effect(request, **kwargs):
        # Verify method change and header cleanup
        assert request.method == 'GET'
        assert request.body is None
        assert 'Content-Length' not in request.headers
        assert 'Content-Type' not in request.headers
        
        resp = requests.Response()
        resp.status_code = 200
        resp.url = request.url
        resp.request = request
        resp._content = b'ok'
        resp._content_consumed = True
        resp.raw = Mock()
        return resp

    with patch.object(session, 'send', side_effect=send_side_effect):
        gen = session.resolve_redirects(initial_resp, initial_req)
        next(gen)