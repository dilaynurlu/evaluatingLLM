import pytest
from unittest.mock import Mock
from requests.sessions import Session
from requests.models import Response, Request

def test_resolve_redirects_schemeless_and_auth_stripping():
    """
    Test that a redirect Location starting with // inherits the scheme (RFC 1808)
    AND that sensitive Authorization headers are stripped when redirecting to a 
    different host (Security).
    """
    session = Session()
    
    # Original URL is HTTPS with Authorization
    url = "https://example.com/secure"
    req = Request(
        method="GET", 
        url=url,
        headers={"Authorization": "Bearer secret_token"}
    ).prepare()
    
    resp = Response()
    resp.status_code = 302
    # Redirect to a different host (cdn.example.com) using schemeless URL
    resp.headers["Location"] = "//cdn.example.com/item"
    resp.url = url
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
    
    # 1. Verify Scheme inheritance (https)
    assert sent_request.url == "https://cdn.example.com/item"
    
    # 2. Verify Authorization header stripping (different host)
    assert "Authorization" not in sent_request.headers