import pytest
import requests
from requests.adapters import HTTPAdapter
from requests.models import Response
from unittest.mock import Mock

def test_resolve_redirects_via_session_get():
    """
    Test resolve_redirects indirectly via session.get() to exercise 
    prepare_request, merge_hooks, and other session logic.
    """
    session = requests.Session()
    
    # Mock the adapter for http://
    adapter = Mock(spec=HTTPAdapter)
    session.mount("http://", adapter)
    
    # Setup the responses
    # 1. Initial response (301)
    resp1 = Response()
    resp1.status_code = 301
    resp1.headers = {"location": "http://example.com/new"}
    resp1.url = "http://example.com/old"
    resp1.reason = "Moved Permanently"
    # We need to set 'connection' on response so requests can release it
    resp1.connection = adapter
    
    # 2. Redirected response (200)
    resp2 = Response()
    resp2.status_code = 200
    resp2.url = "http://example.com/new"
    resp2.reason = "OK"
    resp2.connection = adapter
    
    # Adapter.send side effect to attach request to response (critical for redirects)
    responses = iter([resp1, resp2])
    def send_side_effect(request, *args, **kwargs):
        resp = next(responses)
        resp.request = request
        return resp
        
    adapter.send.side_effect = send_side_effect
    
    # Perform the request
    # This calls prepare_request -> merge_settings -> merge_hooks -> adapter.send -> resolve_redirects
    final_response = session.get("http://example.com/old")
    
    assert final_response.status_code == 200
    assert final_response.url == "http://example.com/new"
    assert len(final_response.history) == 1
    assert final_response.history[0].status_code == 301
    
    # Verify adapter calls
    assert adapter.send.call_count == 2
