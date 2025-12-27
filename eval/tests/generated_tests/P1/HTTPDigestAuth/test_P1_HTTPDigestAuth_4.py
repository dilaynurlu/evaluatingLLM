import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_ignore_missing_digest_header():
    """
    Test that handle_401 returns the original response if the
    WWW-Authenticate header does not contain 'digest'.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = MagicMock(spec=requests.PreparedRequest)
    req.register_hook = MagicMock()
    req.body = None
    auth(req)
    
    r = MagicMock(spec=requests.Response)
    r.status_code = 401
    r.request = req
    # Basic auth challenge instead of Digest
    r.headers = {"www-authenticate": 'Basic realm="foo"'}
    r.connection = MagicMock()
    
    result = auth.handle_401(r)
    
    assert result == r
    assert not r.connection.send.called
    assert auth._thread_local.num_401_calls == 1