import pytest
import requests
from requests.sessions import Session
from requests.models import Request, Response
from unittest.mock import MagicMock

def test_resolve_redirects_auth_stripping_and_method_change():
    """
    Refined test for security and status codes.
    Verifies:
    1. 303 See Other redirects change POST to GET and remove body.
    2. Sensitive headers (Authorization) are STRIPPED when redirecting to a different origin.
    3. Common headers (User-Agent) are preserved.
    """
    session = Session()
    
    # Initial POST request with sensitive Auth header
    origin_url = "http://secure.example.com/api/login"
    target_url = "http://public.example.com/home" # Different domain
    
    headers = {
        "Authorization": "Bearer sensitive_token_123",
        "User-Agent": "TestClient/1.0",
        "Content-Type": "application/json"
    }
    req = Request("POST", origin_url, data='{"user": "test"}', headers=headers).prepare()
    
    # Response triggering 303 redirect
    resp = Response()
    resp.request = req
    resp.url = origin_url
    resp.status_code = 303  # See Other
    resp.headers["Location"] = target_url
    resp._content = b""
    resp._content_consumed = True
    resp.raw = MagicMock()
    
    # Target response
    resp_target = Response()
    resp_target.status_code = 200
    session.send = MagicMock(return_value=resp_target)
    
    # Execute
    gen = session.resolve_redirects(resp, req)
    next(gen)
    
    # Inspect the request passed to send()
    session.send.assert_called_once()
    sent_req = session.send.call_args[0][0]
    
    # 1. Assert Method Change (303 -> GET)
    assert sent_req.method == "GET"
    assert sent_req.body is None
    assert "Content-Length" not in sent_req.headers
    
    # 2. Assert Security: Authorization header must be stripped on cross-origin redirect
    assert "Authorization" not in sent_req.headers
    
    # 3. Assert Non-sensitive headers are preserved
    assert sent_req.headers["User-Agent"] == "TestClient/1.0"
    
    # 4. Assert Host header updated (implied by prepare logic, but good to check if mocked)
    # The PrepareRequest logic updates Host based on URL. Since we mock send, we check the object state.
    assert sent_req.url == target_url