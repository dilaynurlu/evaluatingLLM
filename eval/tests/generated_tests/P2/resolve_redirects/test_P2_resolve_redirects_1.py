import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest

def test_resolve_redirects_follows_302():
    """
    Test that resolve_redirects follows a simple 302 redirect,
    calls send with the new URL, and yields the resulting response.
    """
    session = Session()
    
    # Setup the original request
    original_url = 'http://example.com/start'
    target_url = 'http://example.com/end'
    req = Request('GET', original_url).prepare()
    
    # Setup the initial response that triggers the redirect
    resp = Response()
    resp.status_code = 302
    resp.headers['Location'] = target_url
    resp.url = original_url
    resp.request = req
    # Setup content to avoid raw read
    resp._content = b""
    resp._content_consumed = True
    
    # Setup the response that send() will return
    final_resp = Response()
    final_resp.status_code = 200
    final_resp.url = target_url
    final_resp.request = req.copy()
    final_resp.request.url = target_url
    final_resp._content = b"success"
    final_resp._content_consumed = True
    
    # Mock session.send to return final_resp
    # We patch the instance method
    session.send = Mock(return_value=final_resp)
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    result = next(gen)
    
    # Assertions
    assert result.status_code == 200
    assert result.url == target_url
    
    # Verify send was called with correct parameters
    assert session.send.called
    args, _ = session.send.call_args
    sent_request = args[0]
    assert isinstance(sent_request, PreparedRequest)
    assert sent_request.url == target_url
    assert sent_request.method == 'GET'