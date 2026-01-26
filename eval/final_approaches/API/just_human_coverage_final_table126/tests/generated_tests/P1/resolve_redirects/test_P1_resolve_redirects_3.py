import pytest
from requests.sessions import Session
from requests.models import Request, Response
from unittest.mock import Mock

def test_resolve_redirects_303_post_to_get():
    """
    Test handling of 303 See Other redirect.
    Verifies that a POST request is converted to a GET request,
    and body/headers are stripped appropriately.
    """
    session = Session()
    session.max_redirects = 5
    
    # Original Request: POST with data
    req = Request('POST', 'http://example.com/submit', data={'key': 'value'}).prepare()
    # Sanity check: verify headers were set by prepare()
    assert 'Content-Length' in req.headers
    assert req.body is not None
    
    # First Response: 303 Redirect
    resp1 = Response()
    resp1.status_code = 303  # See Other
    resp1.headers['Location'] = '/resource'
    resp1.url = 'http://example.com/submit'
    resp1._content = b""
    resp1.raw = Mock()
    resp1.request = req
    
    # Second Response: 200 OK
    resp2 = Response()
    resp2.status_code = 200
    resp2.url = 'http://example.com/resource'
    resp2._content = b"OK"
    resp2.raw = Mock()
    
    session.send = Mock(return_value=resp2)
    
    list(session.resolve_redirects(resp1, req))
    
    # Check the request passed to send()
    assert session.send.call_count == 1
    args, _ = session.send.call_args
    sent_req = args[0]
    
    assert sent_req.method == 'GET'
    assert sent_req.url == 'http://example.com/resource'
    assert sent_req.body is None
    # Content-Length and Content-Type should be removed
    assert 'Content-Length' not in sent_req.headers
    assert 'Content-Type' not in sent_req.headers