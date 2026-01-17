import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_simple_chain():
    """
    Test a simple redirect chain: 302 Redirect -> 200 OK.
    Verifies that the function follows the redirect, updates the URL,
    and yields the final response with correct history.
    """
    session = Session()
    
    # Original Request
    original_url = "http://example.com/start"
    target_url = "http://example.com/end"
    
    req = PreparedRequest()
    req.prepare(
        method="GET",
        url=original_url,
        headers={"Host": "example.com"}
    )
    
    # Initial Response (302)
    resp_302 = Response()
    resp_302.status_code = 302
    resp_302.headers["Location"] = target_url
    resp_302.url = original_url
    resp_302.request = req
    resp_302._content = b""
    resp_302._content_consumed = True
    
    # Final Response (200)
    resp_200 = Response()
    resp_200.status_code = 200
    resp_200.url = target_url
    resp_200.request = req.copy()
    resp_200.request.url = target_url
    resp_200._content = b"Success"
    resp_200._content_consumed = True
    
    # Mock session.send to return the final response
    # When send() is called, it should receive the new request targeting target_url
    session.send = Mock(return_value=resp_200)
    
    # Execute
    gen = session.resolve_redirects(resp_302, req)
    results = list(gen)
    
    # Assertions
    assert len(results) == 1
    final_resp = results[0]
    
    assert final_resp.status_code == 200
    assert final_resp.url == target_url
    
    # Verify history
    # The history of the final response should contain the 302 response
    assert len(final_resp.history) == 1
    assert final_resp.history[0] == resp_302
    
    # Verify send was called with correct URL
    args, kwargs = session.send.call_args
    sent_req = args[0]
    assert sent_req.url == target_url