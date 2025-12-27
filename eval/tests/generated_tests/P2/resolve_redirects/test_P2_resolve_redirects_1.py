import pytest
from unittest.mock import patch
import requests
from requests.models import Response, PreparedRequest

def test_resolve_redirects_happy_path_302():
    """
    Test a simple 302 redirect scenario where the client follows to a new location.
    Verifies that the new request is sent to the correct location derived from headers.
    """
    session = requests.Session()
    
    # Prepare the initial request
    req = PreparedRequest()
    req.prepare(
        method='GET',
        url='http://example.com/source',
        headers={'Host': 'example.com'}
    )
    
    # Prepare the initial response (Redirect)
    resp = Response()
    resp.status_code = 302
    resp.headers['Location'] = 'http://example.com/target'
    resp.url = 'http://example.com/source'
    resp.request = req
    resp._content = b''  # Simulate content consumed
    
    # Prepare the mocked response for the followed redirect
    target_resp = Response()
    target_resp.status_code = 200
    target_resp.url = 'http://example.com/target'
    target_resp.request = req.copy()
    target_resp.request.url = 'http://example.com/target'
    target_resp._content = b'Success'
    
    # Mock session.send to avoid actual network usage
    with patch.object(session, 'send', return_value=target_resp) as mock_send:
        generator = session.resolve_redirects(resp, req)
        
        # Advance the generator to follow the redirect
        result = next(generator)
        
        # Assertions
        assert result.status_code == 200
        assert result.url == 'http://example.com/target'
        
        # Verify send was called with correct URL
        args, _ = mock_send.call_args
        sent_request = args[0]
        assert sent_request.url == 'http://example.com/target'
        assert sent_request.method == 'GET'