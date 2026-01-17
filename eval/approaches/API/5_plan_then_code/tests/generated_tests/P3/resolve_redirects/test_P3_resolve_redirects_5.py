import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request

@pytest.mark.parametrize("status_code", [307, 308])
def test_resolve_redirects_method_preserving_codes(status_code):
    """
    Test that 307 (Temporary Redirect) and 308 (Permanent Redirect) 
    preserve the request method (e.g., POST) and body.
    """
    session = Session()
    
    data = "some_data"
    req = Request(method="POST", url="http://example.com/api", data=data).prepare()
    
    resp = Response()
    resp.status_code = status_code
    resp.headers["Location"] = "/api_v2"
    resp.url = "http://example.com/api"
    resp._content = b""
    resp._content_consumed = True
    resp.request = req
    
    resp_next = Response()
    resp_next.status_code = 200
    resp_next._content = b""
    resp_next._content_consumed = True
    
    session.send = Mock(return_value=resp_next)
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    # Verify sent request
    sent_request = session.send.call_args[0][0]
    
    assert sent_request.method == "POST"
    assert sent_request.body == data
    assert sent_request.url == "http://example.com/api_v2"