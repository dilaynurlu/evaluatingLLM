import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Request, Response

def test_resolve_redirects_308_https_downgrade():
    """
    Test HTTP 308 (Permanent Redirect) behavior with HTTPS to HTTP downgrade.
    
    Improvements based on critique:
    1. Tests HTTP 308 (similar to 307) which preserves method (POST) and body.
    2. Verifies SECURITY: Authorization headers must be stripped when 
       downgrading from HTTPS to HTTP, even on the same host.
    """
    session = Session()
    
    # Initial Secure POST request
    req = Request('POST', 'https://secure.example.com/api', 
                  json={'foo': 'bar'},
                  headers={
                      'X-Custom': 'test',
                      'Authorization': 'Bearer secret'
                  })
    prep_req = session.prepare_request(req)
    
    # 308 Response (Permanent Redirect) -> Downgrade to HTTP
    resp = Response()
    resp.status_code = 308
    resp.url = 'https://secure.example.com/api'
    resp.headers['Location'] = 'http://secure.example.com/api_new'
    resp.request = prep_req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()

    # Next Response
    resp_ok = Response()
    resp_ok.status_code = 200
    resp_ok.url = 'http://secure.example.com/api_new'
    resp_ok._content = b"Created"
    resp_ok._content_consumed = True
    resp_ok.raw = MagicMock()
    
    session.send = MagicMock(return_value=resp_ok)
    
    list(session.resolve_redirects(resp, prep_req))
    
    args, _ = session.send.call_args
    sent_req = args[0]
    
    # Method should still be POST (308 behavior)
    assert sent_req.method == 'POST'
    assert sent_req.url == 'http://secure.example.com/api_new'
    
    # Body and safe headers should be preserved
    assert sent_req.body is not None
    assert sent_req.headers['X-Custom'] == 'test'
    
    # SECURITY: Authorization must be removed due to scheme downgrade (https -> http)
    assert 'Authorization' not in sent_req.headers