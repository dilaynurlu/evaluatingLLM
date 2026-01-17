import pytest
from unittest.mock import Mock, MagicMock
from requests import Session, Request, Response

def test_resolve_redirects_307_preserves_post_method():
    """
    Test that a 307 Temporary Redirect preserves the POST method and the body.
    """
    session = Session()
    
    final_resp = Response()
    final_resp.status_code = 200
    final_resp.url = "http://example.com/retry"
    final_resp._content = b"ok"
    final_resp._content_consumed = True
    session.send = Mock(return_value=final_resp)

    # Initial POST Request
    data_payload = "important data"
    req = Request("POST", "http://example.com/submit", data=data_payload).prepare()
    
    # Initial Response (307)
    resp = Response()
    resp.status_code = 307
    resp.headers["Location"] = "http://example.com/retry"
    resp.url = "http://example.com/submit"
    resp.request = req
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()

    # Run
    gen = session.resolve_redirects(resp, req)
    next(gen)

    # Check sent request
    sent_req = session.send.call_args[0][0]
    
    assert sent_req.method == "POST"
    assert sent_req.body == data_payload
    assert "Content-Length" in sent_req.headers
    assert sent_req.url == "http://example.com/retry"