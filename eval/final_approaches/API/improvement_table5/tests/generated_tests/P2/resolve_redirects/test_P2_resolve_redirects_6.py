import pytest
from unittest.mock import Mock, patch
import requests

def test_resolve_redirects_schemeless_url():
    """
    Test handling of redirect locations starting with // (RFC 1808).
    Should inherit scheme from the original request.
    """
    session = requests.Session()
    
    # HTTPS request
    initial_req = requests.Request('GET', 'https://secure.com/resource').prepare()
    
    initial_resp = requests.Response()
    initial_resp.status_code = 302
    # Schemeless redirect
    initial_resp.headers['Location'] = '//cdn.example.com/item'
    initial_resp.url = 'https://secure.com/resource'
    initial_resp.request = initial_req
    initial_resp._content = b''
    initial_resp._content_consumed = True
    initial_resp.raw = Mock()

    def send_side_effect(request, **kwargs):
        # Expect https scheme to be applied
        assert request.url == 'https://cdn.example.com/item'
        
        resp = requests.Response()
        resp.status_code = 200
        resp.url = request.url
        resp.request = request
        resp._content = b''
        resp._content_consumed = True
        resp.raw = Mock()
        return resp

    with patch.object(session, 'send', side_effect=send_side_effect):
        gen = session.resolve_redirects(initial_resp, initial_req)
        next(gen)