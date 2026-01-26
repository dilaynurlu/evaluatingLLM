import pytest
import requests
from requests.sessions import Session
from requests.models import Request, Response
from requests.cookies import RequestsCookieJar
from unittest.mock import MagicMock

def test_resolve_redirects_basic_301_behavior_with_config_and_cookies():
    """
    Refined test for 301 redirects.
    Verifies:
    1. GET redirection works (Basic).
    2. Host header is updated when domain changes.
    3. Request configuration (timeout, verify, proxies) is propagated.
    4. Set-Cookie headers in redirect are persisted to the session.
    """
    session = Session()
    
    # Setup initial request with specific configuration
    url_origin = "http://example.com/origin"
    url_target = "http://other-domain.com/target"
    
    # We set specific config on the request/session to ensure propagation
    req = Request("GET", url_origin).prepare()
    
    # Simulate the kwargs passed to send() which resolve_redirects should propagate
    send_kwargs = {
        "timeout": 30,
        "verify": False,
        "proxies": {"http": "http://proxy.com"},
        "stream": True,
        "cert": "path/to/cert"
    }
    
    # Create the initial response triggering the redirect
    resp_redirect = Response()
    resp_redirect.request = req
    resp_redirect.url = url_origin
    resp_redirect.status_code = 301
    resp_redirect.headers["Location"] = url_target
    resp_redirect.headers["Set-Cookie"] = "session_id=12345; Path=/"
    resp_redirect._content = b""
    resp_redirect._content_consumed = True
    resp_redirect.raw = MagicMock()
    
    # Target response
    resp_final = Response()
    resp_final.status_code = 200
    resp_final.url = url_target
    resp_final.request = req.copy()
    resp_final.request.url = url_target
    
    # Mock session.send
    session.send = MagicMock(return_value=resp_final)
    
    # Execute
    # We assume 'proxies', 'stream', 'verify', 'cert' are passed via kwargs to resolve_redirects 
    # as they typically come from the adapter/session.request flow.
    # However, resolve_redirects signature is (resp, req, stream=False, timeout=None, verify=True, cert=None, proxies=None, ...)
    generator = session.resolve_redirects(
        resp_redirect, 
        req, 
        stream=send_kwargs["stream"],
        timeout=send_kwargs["timeout"],
        verify=send_kwargs["verify"],
        cert=send_kwargs["cert"],
        proxies=send_kwargs["proxies"]
    )
    result_resp = next(generator)
    
    # Assertions
    
    # 1. Cookie Persistence
    assert "session_id" in session.cookies
    assert session.cookies["session_id"] == "12345"
    
    # 2. Verify session.send was called
    session.send.assert_called_once()
    args, kwargs = session.send.call_args
    sent_request = args[0]
    
    # 3. Verify Host header update
    # The Host header should match the new domain
    assert sent_request.headers["Host"] == "other-domain.com"
    
    # 4. Verify Config Propagation
    assert kwargs["timeout"] == 30
    assert kwargs["verify"] is False
    assert kwargs["proxies"] == {"http": "http://proxy.com"}
    assert kwargs["stream"] is True
    assert kwargs["cert"] == "path/to/cert"

    # 5. Verify URL
    assert sent_request.url == url_target