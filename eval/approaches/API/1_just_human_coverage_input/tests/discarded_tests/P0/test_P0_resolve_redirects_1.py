import pytest
from unittest.mock import Mock
from requests import Session, Request, Response

def test_resolve_redirects_basic_flow():
    """
    Test a simple 301 Redirect flow.
    Verifies that the function yields the redirected response and follows the Location header.
    """
    session = Session()
    
    # Prepare the initial request
    req = Request('GET', 'http://example.com/source')
    prep_req = req.prepare()
    
    # Create the first response (301 Moved Permanently)
    resp1 = Response()
    resp1.status_code = 301
    resp1.url = 'http://example.com/source'
    resp1.headers['Location'] = 'http://example.com/target'
    resp1.request = prep_req
    # Simulate consumed content to avoid reading from non-existent raw
    resp1._content = b""
    resp1._content_consumed = True
    
    # Create the second response (200 OK) which should be yielded
    resp2 = Response()
    resp2.status_code = 200
    resp2.url = 'http://example.com/target'
    resp2.request = prep_req  # In reality this would be updated, but for matching check it's okay
    resp2._content = b"Success"
    resp2._content_consumed = True
    
    # Mock session.send to return the final response
    session.send = Mock(return_value=resp2)
    
    # Execute resolve_redirects
    # It returns a generator
    gen = session.resolve_redirects(resp1, prep_req)
    
    # Retrieve the first yielded response
    result = next(gen)
    
    # Assertions
    assert result == resp2
    assert result.history[0] == resp1
    assert result.status_code == 200
    
    # Verify correct URL was requested
    args, _ = session.send.call_args
    sent_request = args[0]
    assert sent_request.url == 'http://example.com/target'
    assert sent_request.method == 'GET'