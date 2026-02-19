import pytest
from unittest.mock import Mock, MagicMock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_basic_302():
    """
    Test a simple 302 redirect scenario.
    Verifies that the function follows the redirect, updates the URL,
    and returns the final successful response.
    """
    session = Session()
    
    # Prepare the initial request
    req = Request('GET', 'http://example.com/start')
    prep_req = session.prepare_request(req)
    
    # Prepare the initial response (302 Redirect)
    resp = Response()
    resp.status_code = 302
    resp.headers['Location'] = 'http://example.com/end'
    resp.url = 'http://example.com/start'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Prepare the next response (200 OK)
    resp_success = Response()
    resp_success.status_code = 200
    resp_success.url = 'http://example.com/end'
    resp_success._content = b"Success"
    resp_success._content_consumed = True
    resp_success.request = None  # In real flow, this would be linked to the new request
    resp_success.raw = MagicMock()
    
    # Mock session.send to return the success response
    # The generator calls session.send(req, ...) to get the next response
    session.send = Mock(return_value=resp_success)
    
    # Execute resolve_redirects
    # It returns a generator yielding responses
    gen = session.resolve_redirects(resp, prep_req)
    
    # Fetch the first yield
    final_resp = next(gen)
    
    # Verify the yielded response is the success response
    assert final_resp.status_code == 200
    assert final_resp.url == 'http://example.com/end'
    
    # Verify session.send was called with the correct redirected URL
    assert session.send.called
    sent_args = session.send.call_args
    sent_request = sent_args[0][0]
    
    assert sent_request.method == 'GET'
    assert sent_request.url == 'http://example.com/end'