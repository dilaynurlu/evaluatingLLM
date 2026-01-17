import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response

def test_resolve_redirects_follows_location():
    """
    Test that resolve_redirects follows a simple 301 Moved Permanently redirect
    by initiating a new request to the location specified in the headers.
    """
    session = Session()
    
    # Define the final response that session.send will return
    final_response = Response()
    final_response.status_code = 200
    final_response.url = "http://example.com/target"
    final_response._content = b"Success"
    final_response._content_consumed = True
    
    # Mock send to avoid network I/O
    session.send = Mock(return_value=final_response)

    # Prepare the initial request
    req = Request("GET", "http://example.com/source").prepare()
    
    # Create the initial response that triggers the redirect
    resp = Response()
    resp.status_code = 301
    resp.headers["Location"] = "http://example.com/target"
    resp.url = "http://example.com/source"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()  # Mock raw to handle close() and read() calls

    # Execute resolve_redirects
    gen = session.resolve_redirects(resp, req)
    result = next(gen)

    # Verify the generator yielded the response from session.send
    assert result.status_code == 200
    assert result.url == "http://example.com/target"
    
    # Verify session.send was called with the correct redirected URL
    assert session.send.call_count == 1
    sent_request = session.send.call_args[0][0]
    assert sent_request.url == "http://example.com/target"
    assert sent_request.method == "GET"