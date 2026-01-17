import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_303_put_to_get():
    """
    Test 303 See Other redirect with a PUT request.
    Critique addressed: Redirecting non-GET/POST methods.
    Should convert the PUT method to GET and remove the body and related headers.
    """
    session = Session()
    
    target_resp = Response()
    target_resp.status_code = 200
    target_resp._content = b"OK"
    target_resp._content_consumed = True
    target_resp.url = "http://example.com/target"
    target_resp.raw = MagicMock()
    
    session.send = MagicMock(return_value=target_resp)
    
    # Initial PUT request with body
    req = PreparedRequest()
    req.prepare(
        method="PUT",
        url="http://example.com/source",
        data="important_update_data"
    )
    
    # Redirect Response (303)
    resp = Response()
    resp.status_code = 303
    resp.headers = CaseInsensitiveDict({"Location": "/target"})
    resp.url = "http://example.com/source"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    resp.request = req
    
    # Execute
    list(session.resolve_redirects(resp, req))
    
    # Verify results
    args, _ = session.send.call_args
    sent_req = args[0]
    
    # Method should be changed to GET
    assert sent_req.method == "GET"
    # Body should be removed
    assert sent_req.body is None
    # Related headers should be purged
    assert "Content-Length" not in sent_req.headers
    assert "Content-Type" not in sent_req.headers