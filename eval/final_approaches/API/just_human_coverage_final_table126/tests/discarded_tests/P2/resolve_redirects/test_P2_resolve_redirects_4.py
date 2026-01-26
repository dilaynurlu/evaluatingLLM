import pytest
from requests.sessions import Session
from requests.models import Request, Response, PreparedRequest

def test_resolve_redirects_307_preserves_post():
    """
    Test that a 307 Temporary Redirect preserves the POST method and the body.
    We use yield_requests=True to verify the prepared request.
    """
    session = Session()
    
    # Initial POST request with data
    data = b'test data'
    req = Request('POST', 'http://example.com/post', data=data).prepare()
    
    # 307 Response
    resp = Response()
    resp.status_code = 307
    resp.headers['Location'] = 'http://example.com/post_new'
    resp.url = 'http://example.com/post'
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    
    # Mock body position to allow rewinding check
    # In a real scenario, requests would check if body is seekable.
    # Here we just verify that the method and body remain on the object yielded.
    req._body_position = 0
    
    # Execute with yield_requests=True
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    new_req = next(gen)
    
    assert isinstance(new_req, PreparedRequest)
    assert new_req.method == 'POST'
    assert new_req.url == 'http://example.com/post_new'
    assert new_req.body == data