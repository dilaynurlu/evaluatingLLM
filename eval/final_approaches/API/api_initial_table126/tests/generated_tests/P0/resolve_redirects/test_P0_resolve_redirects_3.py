import pytest
from unittest.mock import Mock, MagicMock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_post_303_changes_method():
    """
    Test that a 303 See Other redirect on a POST request changes the method to GET
    and drops the body and body-related headers.
    """
    session = Session()
    
    # Initial POST request with data and headers
    req = Request('POST', 'http://example.com/upload', 
                  data={'foo': 'bar'}, 
                  headers={'Content-Type': 'application/x-www-form-urlencoded'})
    prep_req = session.prepare_request(req)
    
    # Confirm initial state
    assert prep_req.method == 'POST'
    assert prep_req.body is not None
    assert 'Content-Length' in prep_req.headers
    
    # Response 303 Redirect
    resp = Response()
    resp.status_code = 303
    resp.headers['Location'] = 'http://example.com/status'
    resp.url = 'http://example.com/upload'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Next response
    resp_next = Response()
    resp_next.status_code = 200
    resp_next.url = 'http://example.com/status'
    resp_next.raw = MagicMock()
    
    session.send = Mock(return_value=resp_next)
    
    gen = session.resolve_redirects(resp, prep_req)
    next(gen)
    
    # Verify the request sent via session.send
    sent_req = session.send.call_args[0][0]
    
    # 303 must switch to GET
    assert sent_req.method == 'GET'
    assert sent_req.url == 'http://example.com/status'
    
    # Body should be None
    assert sent_req.body is None
    
    # Content headers should be purged
    assert 'Content-Length' not in sent_req.headers
    assert 'Content-Type' not in sent_req.headers