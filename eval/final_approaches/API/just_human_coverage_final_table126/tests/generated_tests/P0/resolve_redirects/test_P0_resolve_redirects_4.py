import pytest
from unittest.mock import Mock, MagicMock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_post_307_preserves_method():
    """
    Test that a 307 Temporary Redirect on a POST request preserves the method (POST)
    and includes the original body and headers.
    """
    session = Session()
    
    # Initial POST request
    data = b'{"json": "data"}'
    req = Request('POST', 'http://example.com/api/v1', 
                  data=data, 
                  headers={'Content-Type': 'application/json'})
    prep_req = session.prepare_request(req)
    
    # Response 307 Redirect
    resp = Response()
    resp.status_code = 307
    resp.headers['Location'] = 'http://example.com/api/v2'
    resp.url = 'http://example.com/api/v1'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Next response
    resp_next = Response()
    resp_next.status_code = 200
    resp_next.url = 'http://example.com/api/v2'
    resp_next.raw = MagicMock()
    
    session.send = Mock(return_value=resp_next)
    
    gen = session.resolve_redirects(resp, prep_req)
    next(gen)
    
    sent_req = session.send.call_args[0][0]
    
    # 307 must preserve POST
    assert sent_req.method == 'POST'
    assert sent_req.url == 'http://example.com/api/v2'
    
    # Body and headers should be preserved
    assert sent_req.body == data
    assert sent_req.headers['Content-Type'] == 'application/json'
    assert 'Content-Length' in sent_req.headers