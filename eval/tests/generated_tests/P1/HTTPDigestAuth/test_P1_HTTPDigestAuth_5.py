import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_loop_prevention():
    """
    Test that handle_401 does not retry if num_401_calls reaches limit (2).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = MagicMock(spec=requests.PreparedRequest)
    req.register_hook = MagicMock()
    req.body = None
    auth(req)
    
    # Manually set the call counter to 2
    auth._thread_local.num_401_calls = 2
    
    r = MagicMock(spec=requests.Response)
    r.status_code = 401
    r.request = req
    r.headers = {"www-authenticate": 'Digest realm="foo", nonce="bar", qop="auth"'}
    r.connection = MagicMock()
    r.content = b""
    
    # Since we simulate loop limit reached, it should NOT send again
    result = auth.handle_401(r)
    
    assert result == r
    assert not r.connection.send.called
    # It sets num_401_calls to 1 before returning when failing check?
    # Checking code:
    # if "digest" in ... and self._thread_local.num_401_calls < 2:
    #     ...
    #     return _r
    # self._thread_local.num_401_calls = 1
    # return r
    
    assert auth._thread_local.num_401_calls == 1