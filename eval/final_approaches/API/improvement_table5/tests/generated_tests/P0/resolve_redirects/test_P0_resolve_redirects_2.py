import pytest
from unittest.mock import Mock, patch
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_303_method_change():
    """
    Test a 303 See Other redirect.
    Verifies that a POST request is converted to a GET request and 
    body/content headers are stripped.
    """
    session = Session()
    
    # Setup initial POST request with body and headers
    req = Request('POST', 'http://example.com/post', data='somedata').prepare()
    req.headers['Content-Type'] = 'text/plain'
    req.headers['Content-Length'] = '8'
    
    # Setup 303 redirect response
    resp_redirect = Response()
    resp_redirect.status_code = 303
    resp_redirect.headers['Location'] = 'http://example.com/get'
    resp_redirect.url = 'http://example.com/post'
    resp_redirect.request = req
    resp_redirect.reason = 'See Other'
    resp_redirect._content = b""
    resp_redirect._content_consumed = True
    resp_redirect.raw = Mock()

    # Setup target response
    resp_target = Response()
    resp_target.status_code = 200
    resp_target.url = 'http://example.com/get'
    resp_target._content = b"ok"
    resp_target._content_consumed = True
    resp_target.raw = Mock()

    with patch.object(session, 'send', return_value=resp_target) as mock_send:
        gen = session.resolve_redirects(resp_redirect, req)
        next(gen)
        
        # Check the request passed to send()
        args, _ = mock_send.call_args
        sent_request = args[0]
        
        # Method must change to GET
        assert sent_request.method == 'GET'
        # Body must be removed
        assert sent_request.body is None
        # Content headers must be removed
        assert 'Content-Length' not in sent_request.headers
        assert 'Content-Type' not in sent_request.headers