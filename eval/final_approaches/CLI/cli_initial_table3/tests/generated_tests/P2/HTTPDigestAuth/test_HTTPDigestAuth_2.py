import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
from requests.models import Response, Request
from requests.cookies import RequestsCookieJar

def test_HTTPDigestAuth_handle_401_sha256():
    """
    Test handle_401 with SHA-256 algorithm.
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    # Mock Response
    r = MagicMock(spec=Response)
    r.status_code = 401
    r.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="nonce", algorithm=SHA-256, qop="auth"'
    }
    r.request = MagicMock()
    r.request.url = "http://example.com/foo"
    r.request.method = "POST"
    r.content = b""
    r.connection = MagicMock()
    r.raw = MagicMock()
    
    retried_response = MagicMock(spec=Response)
    retried_response.history = []
    r.connection.send.return_value = retried_response
    
    prep = MagicMock()
    prep.headers = {}
    prep.url = "http://example.com/foo"
    prep.method = "POST"
    prep._cookies = RequestsCookieJar()
    r.request.copy.return_value = prep
    
    result = auth.handle_401(r)
    
    assert result == retried_response
    assert 'algorithm="SHA-256"' in prep.headers["Authorization"]
