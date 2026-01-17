import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response

def test_resolve_redirects_303_post_to_get_method_switch():
    """
    Test that a 303 See Other redirect causes a method switch from POST to GET,
    and removes body/content headers.
    """
    session = Session()
    
    # Mock final response
    final_resp = Response()
    final_resp.status_code = 200
    final_resp.url = "http://example.com/resource"
    final_resp._content = b"ok"
    final_resp._content_consumed = True
    session.send = Mock(return_value=final_resp)

    # Initial POST Request with body and headers
    req = Request("POST", "http://example.com/create", data="some data").prepare()
    # Verify setup preconditions
    assert req.method == "POST"
    assert req.body is not None
    assert "Content-Length" in req.headers

    # Initial Response (303)
    resp = Response()
    resp.status_code = 303
    resp.headers["Location"] = "http://example.com/resource"
    resp.url = "http://example.com/create"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()

    # Run
    gen = session.resolve_redirects(resp, req)
    next(gen)

    # Check the request sent by session.send
    sent_req = session.send.call_args[0][0]
    
    assert sent_req.method == "GET"
    assert sent_req.body is None
    assert "Content-Length" not in sent_req.headers
    assert "Content-Type" not in sent_req.headers
    assert sent_req.url == "http://example.com/resource"