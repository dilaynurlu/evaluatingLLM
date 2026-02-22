import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
from requests.models import Request

def test_HTTPDigestAuth_call_hooks():
    """
    Test that __call__ registers hooks on the request.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock Request
    r = MagicMock(spec=Request)
    r.headers = {}
    
    # Mock body.tell() behavior
    r.body = MagicMock()
    r.body.tell.return_value = 0
    
    # Call auth
    result = auth(r)
    
    assert result == r
    # Verify hooks registered
    assert r.register_hook.call_count == 2
    
    calls = r.register_hook.call_args_list
    assert calls[0][0][0] == "response"
    assert calls[0][0][1] == auth.handle_401
    
    assert calls[1][0][0] == "response"
    assert calls[1][0][1] == auth.handle_redirect
