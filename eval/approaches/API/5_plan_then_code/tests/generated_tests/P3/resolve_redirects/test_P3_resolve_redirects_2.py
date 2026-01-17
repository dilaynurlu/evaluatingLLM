import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_relative_url():
    """
    Test that resolve_redirects correctly handles a relative URL in the Location header,
    resolving it against the original URL.
    """
    session = Session()
    
    # Initial setup
    base_url = "http://example.com/path/resource"
    req = Request(method="GET", url=base_url).prepare()
    
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "../new_resource"
    resp.url = base_url
    resp._content = b""
    resp._content_consumed = True
    resp.request = req
    
    # Mock the next response
    resp_next = Response()
    resp_next.status_code = 200
    resp_next.url = "http://example.com/new_resource"
    resp_next._content = b"Success"
    resp_next._content_consumed = True
    
    # Capture the request passed to send to verify URL resolution
    session.send = Mock(return_value=resp_next)
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    result_resp = next(gen)
    
    # Verify the response
    assert result_resp == resp_next
    
    # Verify the URL in the request passed to send was resolved correctly
    # ../new_resource from /path/resource -> /new_resource
    call_args = session.send.call_args
    sent_request = call_args[0][0]
    assert sent_request.url == "http://example.com/new_resource"