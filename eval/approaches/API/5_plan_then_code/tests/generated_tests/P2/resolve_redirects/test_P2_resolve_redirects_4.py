import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_method_change_303():
    """
    Test that a POST request redirected via 303 See Other is converted to GET,
    and the body and body-related headers are removed.
    """
    session = Session()
    
    initial_url = 'http://example.com/form'
    target_url = 'http://example.com/result'
    
    # Create a POST request with body and headers
    req = Request('POST', initial_url, data={'key': 'value'}, headers={'Content-Type': 'application/x-www-form-urlencoded'}).prepare()
    # Verify setup preconditions
    assert req.method == 'POST'
    assert req.body is not None
    assert 'Content-Length' in req.headers
    
    resp = Response()
    resp.status_code = 303  # See Other -> Must change to GET
    resp.url = initial_url
    resp.headers['Location'] = target_url
    resp._content = b''
    resp._content_consumed = True
    resp.request = req
    
    captured_requests = []
    def side_effect(request, **kwargs):
        captured_requests.append(request)
        r = Response()
        r.status_code = 200
        r.url = request.url
        r._content = b'OK'
        r._content_consumed = True
        return r
        
    session.send = Mock(side_effect=side_effect)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    sent_req = captured_requests[0]
    
    # RFC 7231: 303 redirects MUST be GET
    assert sent_req.method == 'GET'
    assert sent_req.url == target_url
    assert sent_req.body is None
    assert 'Content-Length' not in sent_req.headers
    assert 'Content-Type' not in sent_req.headers