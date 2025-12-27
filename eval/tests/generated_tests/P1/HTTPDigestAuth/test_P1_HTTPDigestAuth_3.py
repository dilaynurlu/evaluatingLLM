import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_ignore_non_401_status():
    """
    Test that handle_401 returns the original response unmodified
    if the status code is not 401 (e.g., 200 or 500).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Init call
    req = MagicMock(spec=requests.PreparedRequest)
    req.register_hook = MagicMock()
    req.body = None
    auth(req)
    
    # Response with 200 OK
    r = MagicMock(spec=requests.Response)
    r.status_code = 200
    r.request = req
    r.headers = {"www-authenticate": 'Digest realm="foo", nonce="bar"'} # Should be ignored due to status
    r.connection = MagicMock()
    
    result = auth.handle_401(r)
    
    # Should return original response
    assert result == r
    # Should not attempt to send new request
    assert not r.connection.send.called
    # Counter should be reset
    assert auth._thread_local.num_401_calls == 1