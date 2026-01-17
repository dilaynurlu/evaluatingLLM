import pytest
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_HTTPDigestAuth_call_hook_registration():
    auth = HTTPDigestAuth("user", "pass")
    r = Mock()
    r.headers = {}
    r.body = Mock()
    
    auth(r)
    
    # Check that hooks were registered
    assert r.register_hook.call_count == 2
    calls = r.register_hook.call_args_list
    assert calls[0][0][0] == 'response'
    assert calls[0][0][1] == auth.handle_401
    assert calls[1][0][0] == 'response'
    assert calls[1][0][1] == auth.handle_redirect
