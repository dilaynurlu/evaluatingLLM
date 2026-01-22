import pytest
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest

def test_resolve_redirects_303_changes_to_get():
    """
    Test that a 303 See Other redirect changes the request method to GET
    and removes the body. We use yield_requests=True to verify the prepared request.
    """
    session = Session()
    
    # Initial POST request with data
    req = Request('POST', 'http://example.com/post', data={'key': 'value'}).prepare()
    assert req.method == 'POST'
    assert req.body is not None
    
    # 303 Response
    resp = Response()
    resp.status_code = 303
    resp.headers['Location'] = 'http://example.com/get'
    resp.url = 'http://example.com/post'
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    
    # Execute with yield_requests=True
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    new_req = next(gen)
    
    assert isinstance(new_req, PreparedRequest)
    assert new_req.method == 'GET'
    assert new_req.url == 'http://example.com/get'
    assert new_req.body is None
    # Content related headers should be popped
    assert 'Content-Length' not in new_req.headers
    assert 'Content-Type' not in new_req.headers