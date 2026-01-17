import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_308_preserves_put_method():
    """
    Test 308 Permanent Redirect with a PUT request.
    Critique addressed: Missing HTTP 308 Support, Redirecting non-GET/POST methods.
    Should preserve the PUT method and the body.
    """
    session = Session()
    
    target_resp = Response()
    target_resp.status_code = 200
    target_resp._content = b"OK"
    target_resp._content_consumed = True
    target_resp.url = "http://example.com/target"
    target_resp.raw = MagicMock()
    
    session.send = MagicMock(return_value=target_resp)
    
    # Request: PUT with body
    req = PreparedRequest()
    req.prepare(
        method="PUT",
        url="http://example.com/source",
        data="original_put_data"
    )
    
    # Response: 308
    resp = Response()
    resp.status_code = 308
    resp.headers = CaseInsensitiveDict({"Location": "/target"})
    resp.url = "http://example.com/source"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    resp.request = req
    
    # Execute
    list(session.resolve_redirects(resp, req))
    
    args, _ = session.send.call_args
    sent_req = args[0]
    
    # Assert method preserved
    assert sent_req.method == "PUT"
    
    # Assert body preserved
    assert sent_req.body == b"original_put_data"
    
    # Assert Content-Length preserved
    assert "Content-Length" in sent_req.headers
    assert sent_req.headers["Content-Length"] == str(len(b"original_put_data"))