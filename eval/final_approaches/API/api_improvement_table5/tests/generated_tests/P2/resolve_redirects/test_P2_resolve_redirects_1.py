import pytest
from unittest.mock import Mock, patch
import requests
from requests.exceptions import TooManyRedirects

def test_resolve_redirects_max_limit():
    """
    Test that TooManyRedirects is raised when the number of redirects exceeds the configured max_redirects.
    """
    session = requests.Session()
    session.max_redirects = 2
    
    # Create the initial response that triggers the redirect chain
    # Initial: GET /start -> 302 /redirect1
    initial_req = requests.Request('GET', 'http://example.com/start').prepare()
    initial_resp = requests.Response()
    initial_resp.status_code = 302
    initial_resp.headers['Location'] = '/redirect1'
    initial_resp.url = 'http://example.com/start'
    initial_resp.request = initial_req
    initial_resp._content = b''
    initial_resp._content_consumed = True
    initial_resp.raw = Mock()

    # Define a side effect that returns subsequent redirect responses based on the requested URL
    def send_side_effect(request, **kwargs):
        # Extract counter from URL (e.g., /redirect1 -> 1)
        path = request.url.split('/')[-1]
        if path.startswith('redirect'):
            count = int(path.replace('redirect', ''))
        else:
            count = 0
            
        resp = requests.Response()
        resp.status_code = 302
        resp.request = request
        resp.url = request.url
        resp._content = b''
        resp._content_consumed = True
        resp.raw = Mock()
        
        # Point to the next redirect
        resp.headers['Location'] = f'/redirect{count + 1}'
        return resp

    # We expect:
    # 1. resolve_redirects called with initial (pointing to /redirect1).
    # 2. send() called for /redirect1 -> returns 302 to /redirect2. Yields response.
    # 3. send() called for /redirect2 -> returns 302 to /redirect3. Yields response.
    # 4. Preparation for /redirect3 detects history length >= 2 (initial + redirect1 + redirect2? No, history accumulation).
    #    Actually: 
    #    - Loop 1: hist=[initial]. len=0. send(/redirect1). Yields resp1.
    #    - Loop 2: hist=[initial, resp1]. len=1. send(/redirect2). Yields resp2.
    #    - Loop 3: hist=[initial, resp1, resp2]. len=2. 2 >= 2 -> Raise.
    
    with patch.object(session, 'send', side_effect=send_side_effect):
        gen = session.resolve_redirects(initial_resp, initial_req)
        
        # 1st yield: Response for /redirect1
        r1 = next(gen)
        assert 'redirect1' in r1.url
        
        # 2nd yield: Response for /redirect2
        r2 = next(gen)
        assert 'redirect2' in r2.url
        
        # 3rd attempt should raise
        with pytest.raises(TooManyRedirects) as excinfo:
            next(gen)
        assert "Exceeded 2 redirects" in str(excinfo.value)