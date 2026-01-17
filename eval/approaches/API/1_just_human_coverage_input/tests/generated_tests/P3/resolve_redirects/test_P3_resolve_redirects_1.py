import pytest
from unittest.mock import MagicMock
from requests.sessions import Session
from requests.models import Response, PreparedRequest
from requests.structures import CaseInsensitiveDict

def test_resolve_redirects_cross_domain_strips_auth():
    """
    Test a 301 redirect to a different domain.
    Critique addressed: Missing Cross-Domain Header Stripping Tests.
    Should verify that sensitive headers (Authorization) are stripped when redirecting to a new host.
    """
    session = Session()
    
    # Target response (new domain)
    target_resp = Response()
    target_resp.status_code = 200
    target_resp._content = b"Target Content"
    target_resp._content_consumed = True
    target_resp.url = "http://other.com/target"
    target_resp.raw = MagicMock()
    
    session.send = MagicMock(return_value=target_resp)
    
    # Initial request with sensitive headers
    req = PreparedRequest()
    req.prepare(
        method="GET",
        url="http://example.com/source",
        headers={"Authorization": "Bearer secret_token"}
    )
    
    # Initial response (Redirect to different host)
    resp = Response()
    resp.status_code = 301
    resp.headers = CaseInsensitiveDict({"Location": "http://other.com/target"})
    resp.url = "http://example.com/source"
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    resp.request = req
    
    # Execute
    results = list(session.resolve_redirects(resp, req))
    
    # Verify
    assert len(results) == 1
    
    # Check the request sent to the new domain
    args, _ = session.send.call_args
    sent_req = args[0]
    
    assert sent_req.url == "http://other.com/target"
    # Authorization header should have been removed
    assert "Authorization" not in sent_req.headers