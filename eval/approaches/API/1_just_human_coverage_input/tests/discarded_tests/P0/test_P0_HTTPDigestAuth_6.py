import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_http_digest_auth_retry_limit():
    """
    Test that handle_401 does NOT retry if the number of 401 calls exceeds the limit (2).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.org/"
    req.headers = {}
    req.hooks = {"response": []}
    
    auth(req)
    
    # Manually set the state to simulate that we have already tried responding to a challenge
    auth._thread_local.num_401_calls = 2
    
    resp = Mock(spec=Response)
    resp.request = req
    resp.status_code = 401
    resp.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="newnonce", algorithm="MD5"'
    }
    resp.content = b""
    resp.raw = Mock()
    resp.raw._original_response = None
    resp.connection = Mock()
    
    # handle_401 should return the original response without retrying
    result = auth.handle_401(resp)
    
    assert result == resp
    assert not resp.connection.send.called
    # Counter should not increment past 2 (or just stays high)
    assert auth._thread_local.num_401_calls == 2