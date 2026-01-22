import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_303_post_to_get():
    """
    Test 303 See Other behavior with Cross-Domain security check.
    
    Improvements based on critique:
    1. Verifies 303 converts POST to GET and drops body.
    2. Verifies SECURITY: Authorization headers must be stripped when 
       redirecting to a different host (Cross-Domain).
    """
    session = Session()
    
    # Initial POST request with body and sensitive headers
    req = Request('POST', 'http://example.com/submit', 
                  data={'key': 'value'}, 
                  headers={
                      'Content-Type': 'application/x-www-form-urlencoded',
                      'Authorization': 'Bearer secret_token'
                  })
    prep_req = session.prepare_request(req)
    
    assert 'Authorization' in prep_req.headers

    # 303 Response redirecting to a DIFFERENT HOST
    resp = Response()
    resp.status_code = 303
    resp.url = 'http://example.com/submit'
    resp.headers['Location'] = 'http://other-site.com/result'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()

    # Next Response
    resp_ok = Response()
    resp_ok.status_code = 200
    resp_ok.url = 'http://other-site.com/result'
    resp_ok._content = b"OK"
    resp_ok._content_consumed = True
    resp_ok.raw = MagicMock()
    
    session.send = MagicMock(return_value=resp_ok)
    
    # Execute
    list(session.resolve_redirects(resp, prep_req))
    
    # Check the request sent
    args, _ = session.send.call_args
    sent_req = args[0]
    
    # 1. Method converted to GET, Body dropped
    assert sent_req.method == 'GET'
    assert sent_req.url == 'http://other-site.com/result'
    assert sent_req.body is None
    assert 'Content-Length' not in sent_req.headers
    
    # 2. Security: Authorization header stripped on cross-domain redirect
    assert 'Authorization' not in sent_req.headers