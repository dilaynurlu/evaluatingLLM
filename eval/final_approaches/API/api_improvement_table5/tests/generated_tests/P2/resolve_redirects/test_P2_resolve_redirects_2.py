import pytest
from unittest.mock import Mock, patch
import requests

def test_resolve_redirects_307_preserves_post():
    """
    Test that a 307 Temporary Redirect preserves the POST method and the request body.
    """
    session = requests.Session()
    
    # Prepare a POST request with body
    initial_req = requests.Request(
        'POST', 
        'http://example.com/post', 
        data='test_data',
        headers={'Content-Type': 'text/plain'}
    ).prepare()
    
    initial_resp = requests.Response()
    initial_resp.status_code = 307
    initial_resp.headers['Location'] = '/target'
    initial_resp.url = 'http://example.com/post'
    initial_resp.request = initial_req
    initial_resp._content = b''
    initial_resp._content_consumed = True
    initial_resp.raw = Mock()

    # Mock send to verify the request it receives has not been downgraded to GET
    def send_side_effect(request, **kwargs):
        assert request.method == 'POST'
        assert request.body == 'test_data'
        
        resp = requests.Response()
        resp.status_code = 200
        resp.url = request.url
        resp.request = request
        resp._content = b'ok'
        resp._content_consumed = True
        resp.raw = Mock()
        return resp

    with patch.object(session, 'send', side_effect=send_side_effect) as mock_send:
        gen = session.resolve_redirects(initial_resp, initial_req)
        final_resp = next(gen)
        
        assert final_resp.status_code == 200
        assert final_resp.url == 'http://example.com/target'
        mock_send.assert_called_once()