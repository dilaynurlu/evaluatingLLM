import pytest
from unittest.mock import Mock
from requests import Session, Request, Response

def test_resolve_redirects_303_method_change():
    """
    Test that a 303 See Other redirect changes a POST request to a GET request
    and drops the body/headers.
    """
    session = Session()
    
    # Initial POST request with data
    req = Request('POST', 'http://example.com/submit', data={'foo': 'bar'})
    prep_req = req.prepare()
    
    # Verify initial state
    assert prep_req.method == 'POST'
    assert prep_req.body is not None
    assert 'Content-Length' in prep_req.headers
    
    # Response is 303 Redirect
    resp = Response()
    resp.status_code = 303
    resp.url = 'http://example.com/submit'
    resp.headers['Location'] = '/thank-you'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    
    # Mock next response
    resp_next = Response()
    resp_next.status_code = 200
    resp_next.url = 'http://example.com/thank-you'
    resp_next._content = b"Done"
    resp_next._content_consumed = True
    
    session.send = Mock(return_value=resp_next)
    
    # Execute
    gen = session.resolve_redirects(resp, prep_req)
    next(gen)
    
    # Inspect the request sent via session.send
    args, _ = session.send.call_args
    sent_req = args[0]
    
    # Assertions for 303 behavior
    assert sent_req.method == 'GET'
    assert sent_req.url == 'http://example.com/thank-you'
    assert sent_req.body is None
    assert 'Content-Length' not in sent_req.headers
    assert 'Content-Type' not in sent_req.headers