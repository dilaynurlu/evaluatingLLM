import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_303_post_to_get_rewrite():
    """
    Test that a 303 See Other redirect changes a POST request to a GET request,
    and removes body-related headers (Content-Length, Content-Type, Transfer-Encoding).
    """
    session = Session()
    
    # Original POST request with body
    req = Request('POST', 'http://example.com/post', data={'a': 'b'}).prepare()
    # verify setup
    assert 'Content-Length' in req.headers
    
    # 303 Response
    resp = Response()
    resp.status_code = 303
    resp.url = 'http://example.com/post'
    resp.headers = CaseInsensitiveDict({'Location': 'http://example.com/get'})
    resp.raw = MagicMock()
    
    final_resp = Response()
    final_resp.status_code = 200
    
    session.send = Mock(return_value=final_resp)
    
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    # Verify send was called with GET and no body
    called_req = session.send.call_args[0][0]
    
    assert called_req.method == 'GET'
    assert called_req.url == 'http://example.com/get'
    assert called_req.body is None
    
    # Content headers should be popped
    assert 'Content-Length' not in called_req.headers
    assert 'Content-Type' not in called_req.headers
    assert 'Transfer-Encoding' not in called_req.headers