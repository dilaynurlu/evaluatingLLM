import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request

@pytest.mark.parametrize("status_code", [301, 302, 303])
def test_resolve_redirects_method_changing_codes(status_code):
    """
    Test that 301, 302, and 303 redirects change the method from POST to GET
    and remove the body and body-related headers (Content-*, Transfer-Encoding).
    """
    session = Session()
    
    # Initial POST request with body and headers
    req = Request(
        method="POST", 
        url="http://example.com/submit", 
        data={"key": "value"},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Transfer-Encoding": "chunked"
        }
    ).prepare()
    
    resp = Response()
    resp.status_code = status_code
    resp.headers["Location"] = "/thank-you"
    resp.url = "http://example.com/submit"
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
    
    # Method should be changed to GET
    assert sent_request.method == "GET"
    # Body should be None
    assert sent_request.body is None
    # Content and Transfer-Encoding headers should be removed
    assert "Content-Length" not in sent_request.headers
    assert "Content-Type" not in sent_request.headers
    assert "Transfer-Encoding" not in sent_request.headers