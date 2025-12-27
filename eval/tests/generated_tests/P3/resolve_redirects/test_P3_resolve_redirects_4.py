import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_303_method_change_and_cleanup():
    """
    Test that a 303 See Other redirect correctly forces the method to GET
    and removes body-related headers (Content-Length, Content-Type).
    """
    session = Session()
    
    # Original POST request with body and headers
    req = PreparedRequest()
    req.prepare(
        method='POST', 
        url="http://example.com/post", 
        headers={'Content-Length': '123', 'Content-Type': 'application/json', 'X-Custom': 'KeepMe'},
        data='{"foo": "bar"}'
    )
    
    # Response triggering 303
    resp = Response()
    resp.status_code = 303
    resp.url = "http://example.com/post"
    resp.headers['Location'] = "http://example.com/get"
    resp._content = b""
    
    # Mock send - return a dummy successful response
    session.send = MagicMock(return_value=Response())
    session.send.return_value._content = b""
    
    # Use yield_requests=True to inspect the PreparedRequest object generated for the redirect
    gen = session.resolve_redirects(resp, req, yield_requests=True)
    redirected_req = next(gen)
    
    # Assert Method Change
    assert redirected_req.method == 'GET'
    assert redirected_req.url == "http://example.com/get"
    
    # Assert Header Cleanup
    assert 'Content-Length' not in redirected_req.headers
    assert 'Content-Type' not in redirected_req.headers
    assert redirected_req.headers['X-Custom'] == 'KeepMe' # Should preserve other headers
    
    # Assert Body Cleanup
    assert redirected_req.body is None