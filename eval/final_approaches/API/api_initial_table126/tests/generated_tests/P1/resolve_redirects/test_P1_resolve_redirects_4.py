import pytest
from requests.sessions import Session
from requests.models import Request, Response
from unittest.mock import Mock

def test_resolve_redirects_relative_location():
    """
    Test that a relative 'Location' header is correctly joined with the
    original response URL.
    """
    session = Session()
    session.max_redirects = 5
    
    req = Request('GET', 'http://example.com/path/one').prepare()
    
    # Redirect to a relative path
    resp1 = Response()
    resp1.status_code = 301
    resp1.headers['Location'] = 'two'  # Relative path
    resp1.url = 'http://example.com/path/one'
    resp1._content = b""
    resp1.raw = Mock()
    resp1.request = req
    
    resp2 = Response()
    resp2.status_code = 200
    resp2.url = 'http://example.com/path/two'
    resp2._content = b"OK"
    resp2.raw = Mock()
    
    session.send = Mock(return_value=resp2)
    
    list(session.resolve_redirects(resp1, req))
    
    assert session.send.call_count == 1
    args, _ = session.send.call_args
    sent_req = args[0]
    
    # Should resolve relative to http://example.com/path/one -> http://example.com/path/two
    assert sent_req.url == 'http://example.com/path/two'