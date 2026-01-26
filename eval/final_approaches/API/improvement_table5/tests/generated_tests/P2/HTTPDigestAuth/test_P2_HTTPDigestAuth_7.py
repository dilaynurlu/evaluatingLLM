import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_redirect_reset():
    """
    Test that handle_redirect resets the 401 call counter.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req)
    
    # Simulate a state where we have already tried auth once
    auth._thread_local.num_401_calls = 2
    
    resp = Response()
    resp.status_code = 302
    resp.headers["Location"] = "/new"
    
    # Find handle_redirect hook
    handle_redirect_hook = None
    for hook in req.hooks["response"]:
        if getattr(hook, "__name__", "") == "handle_redirect":
            handle_redirect_hook = hook
            break
    assert handle_redirect_hook is not None
    
    # Trigger redirect hook
    handle_redirect_hook(resp)
    
    # Assert counter is reset to 1
    assert auth._thread_local.num_401_calls == 1