import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_basic_302():
    """
    Test a simple HTTP 302 redirect.
    Verifies that the function follows the redirect, updates the URL,
    and yields the response returned by the session's send method.
    """
    session = Session()
    
    # 1. Prepare the initial request
    initial_url = 'http://example.com/start'
    target_url = 'http://example.com/end'
    req = Request('GET', initial_url).prepare()
    
    # 2. Prepare the initial response (redirect)
    resp = Response()
    resp.status_code = 302
    resp.url = initial_url
    resp.headers['Location'] = target_url
    # Ensure content is consumed to avoid IO ops
    resp._content = b''
    resp._content_consumed = True
    resp.request = req
    
    # 3. Prepare the next response (target)
    next_resp = Response()
    next_resp.status_code = 200
    next_resp.url = target_url
    next_resp._content = b'OK'
    next_resp._content_consumed = True
    
    # 4. Mock session.send to return the target response
    # We use a side_effect to capture the request passed to send
    captured_requests = []
    def side_effect(request, **kwargs):
        captured_requests.append(request)
        next_resp.request = request
        return next_resp
        
    session.send = Mock(side_effect=side_effect)
    
    # 5. Execute resolve_redirects
    # It returns a generator
    gen = session.resolve_redirects(resp, req)
    
    # 6. Iterate to get the first result
    result = next(gen)
    
    # 7. Assertions
    assert result == next_resp
    assert result.status_code == 200
    assert result.url == target_url
    
    # Verify the request sent to session.send
    assert len(captured_requests) == 1
    sent_req = captured_requests[0]
    assert sent_req.url == target_url
    assert sent_req.method == 'GET'