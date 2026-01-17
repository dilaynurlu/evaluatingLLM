import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_method_change_303():
    """
    Test handling of 303 See Other:
    - Method should change to GET.
    - Body should be dropped.
    - Content-* headers should be purged.
    """
    session = Session()
    
    req = PreparedRequest()
    # Prepare a POST request with body and headers
    headers = {
        'Content-Length': '100', 
        'Content-Type': 'application/json', 
        'Transfer-Encoding': 'chunked', 
        'X-Custom': 'KeepMe'
    }
    req.prepare(method='POST', url='http://example.com/post', headers=headers)
    req.body = b"payload"
    
    resp1 = Response()
    resp1.status_code = 303
    resp1.headers['Location'] = '/get'
    resp1.url = 'http://example.com/post'
    resp1.request = req
    resp1._content = b""
    resp1._content_consumed = True
    resp1.raw = MagicMock()
    
    captured_req = []

    def send_mock(request, **kwargs):
        captured_req.append(request)
        # Return a final response to stop recursion
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        resp._content = b""
        resp._content_consumed = True
        resp.raw = MagicMock()
        return resp

    session.send = MagicMock(side_effect=send_mock)
    
    list(session.resolve_redirects(resp1, req))
    
    assert len(captured_req) == 1
    sent_req = captured_req[0]
    
    # Verify method changed to GET (Session.rebuild_method behavior for 303)
    assert sent_req.method == 'GET'
    
    # Verify headers purged
    assert 'Content-Length' not in sent_req.headers
    assert 'Content-Type' not in sent_req.headers
    assert 'Transfer-Encoding' not in sent_req.headers
    assert sent_req.headers['X-Custom'] == 'KeepMe'
    
    # Verify body dropped
    assert sent_req.body is None