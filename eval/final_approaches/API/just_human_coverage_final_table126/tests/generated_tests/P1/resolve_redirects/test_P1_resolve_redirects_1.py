import pytest
from requests.sessions import Session
from requests.models import Request, Response
from unittest.mock import Mock

def test_resolve_redirects_simple_301():
    """
    Test a simple 301 Moved Permanently redirect.
    Verifies that the method follows the redirect, updates the URL,
    calls send() with the new request, and yields the resulting response.
    """
    session = Session()
    # Mock the send method to prevent actual network calls
    # The first call to resolve_redirects is with the original response (301).
    # resolve_redirects will verify the location and call session.send() for the new URL.
    
    # Original prepared request
    req = Request('GET', 'http://example.com/old').prepare()
    
    # The initial response that triggers the redirect
    resp1 = Response()
    resp1.status_code = 301
    resp1.headers['Location'] = 'http://example.com/new'
    resp1.url = 'http://example.com/old'
    resp1._content = b""  # Pre-consumed content
    resp1.raw = Mock()    # Mock raw to support close()
    resp1.request = req
    
    # The expected second response (Success)
    resp2 = Response()
    resp2.status_code = 200
    resp2.url = 'http://example.com/new'
    resp2._content = b"Success"
    resp2.raw = Mock()
    resp2.request = None # resolve_redirects will assign the new request to this if yielded? 
                         # Actually resolve_redirects yields what send() returns.
    
    session.send = Mock(return_value=resp2)
    session.max_redirects = 30
    
    # Execute
    gen = session.resolve_redirects(resp1, req)
    results = list(gen)
    
    # Assertions
    assert len(results) == 1
    assert results[0] is resp2
    assert results[0].status_code == 200
    
    # Verify session.send was called with the correct URL
    assert session.send.call_count == 1
    args, kwargs = session.send.call_args
    sent_request = args[0]
    
    assert sent_request.url == 'http://example.com/new'
    assert sent_request.method == 'GET'