import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, PreparedRequest

def test_resolve_redirects_303_cleanup():
    """
    Test that a 303 Redirect causes the request method to change to GET (via rebuild_method)
    and removes body-related headers (Content-Length, Content-Type, Transfer-Encoding).
    """
    session = Session()
    
    # Initial POST request with body and content headers
    req = PreparedRequest()
    req.prepare(
        method="POST",
        url="http://example.com/post",
        data="some data",
        headers={"Content-Type": "text/plain", "Extra-Header": "KeepMe"}
    )
    # req.prepare automatically adds Content-Length
    assert "Content-Length" in req.headers
    assert req.body is not None
    
    # 303 Response
    resp = Response()
    resp.status_code = 303
    resp.headers["Location"] = "http://example.com/get"
    resp.url = "http://example.com/post"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    
    # Next response (200 OK)
    resp_200 = Response()
    resp_200.status_code = 200
    resp_200.url = "http://example.com/get"
    resp_200._content = b""
    resp_200._content_consumed = True
    
    # Mock send
    session.send = Mock(return_value=resp_200)
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    list(gen) # consume generator
    
    # Check what was sent
    assert session.send.called
    sent_req = session.send.call_args[0][0]
    
    # Verify Headers cleaned
    assert "Content-Length" not in sent_req.headers
    assert "Content-Type" not in sent_req.headers
    assert "Transfer-Encoding" not in sent_req.headers
    assert "Extra-Header" in sent_req.headers  # Should remain
    
    # Verify Body removed
    assert sent_req.body is None
    
    # Verify Method changed to GET (Standard behavior for 303 in requests Session)
    # resolve_redirects calls self.rebuild_method. 
    # Since we use a real Session object, it should perform the switch for 303.
    assert sent_req.method == "GET"