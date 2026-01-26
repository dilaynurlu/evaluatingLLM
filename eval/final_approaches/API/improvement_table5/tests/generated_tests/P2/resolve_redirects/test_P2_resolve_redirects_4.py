import pytest
from unittest.mock import Mock, patch
import requests

def test_resolve_redirects_fragment_handling():
    """
    Test that URL fragments are maintained across redirects unless the redirect URL explicitly defines a new fragment.
    """
    session = requests.Session()
    
    # Initial request has a fragment
    initial_req = requests.Request('GET', 'http://example.com/page#section1').prepare()
    
    initial_resp = requests.Response()
    initial_resp.status_code = 302
    initial_resp.headers['Location'] = '/intermediate'  # No fragment here
    initial_resp.url = 'http://example.com/page#section1'
    initial_resp.request = initial_req
    initial_resp._content = b''
    initial_resp._content_consumed = True
    initial_resp.raw = Mock()

    # Chain:
    # 1. /page#section1 -> 302 /intermediate (Expects #section1 to be carried over)
    # 2. /intermediate#section1 -> 302 /final#section2 (Expects #section2 to override)
    
    def send_side_effect(request, **kwargs):
        resp = requests.Response()
        resp.request = request
        resp.url = request.url
        resp._content = b''
        resp._content_consumed = True
        resp.raw = Mock()
        
        if request.url == 'http://example.com/intermediate#section1':
            resp.status_code = 302
            resp.headers['Location'] = '/final#section2'
            return resp
        elif request.url == 'http://example.com/final#section2':
            resp.status_code = 200
            return resp
        else:
            pytest.fail(f"Unexpected URL requested: {request.url}")

    with patch.object(session, 'send', side_effect=send_side_effect):
        gen = session.resolve_redirects(initial_resp, initial_req)
        
        # First redirect: Should have original fragment
        resp1 = next(gen)
        assert resp1.url == 'http://example.com/intermediate#section1'
        
        # Second redirect: Should have new fragment
        resp2 = next(gen)
        assert resp2.url == 'http://example.com/final#section2'