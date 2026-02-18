import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_call():
    """Test __call__ hooks registration."""
    auth = HTTPDigestAuth("user", "pass")
    req = Mock()
    req.headers = {}
    req.register_hook = Mock()
    
    auth(req)
    
    assert req.register_hook.call_count == 2
    # Checks that hooks are registered
    args = req.register_hook.call_args_list
    assert args[0][0][0] == "response"
    assert args[0][0][1] == auth.handle_401
    assert args[1][0][0] == "response"
    assert args[1][0][1] == auth.handle_redirect
