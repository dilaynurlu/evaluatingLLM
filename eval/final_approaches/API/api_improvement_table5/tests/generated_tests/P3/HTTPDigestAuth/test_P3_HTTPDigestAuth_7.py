import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_retry_limit():
    """
    Test that the authentication handler respects the retry limit.
    Refined to rely on natural state transitions by calling handle_401 sequentially.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com/").prepare()
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers = CaseInsensitiveDict({
        "www-authenticate": 'Digest realm="realm", nonce="nonce", qop="auth"'
    })
    resp.raw = Mock()
    resp._content = b""
    resp.connection = Mock()
    resp.connection.send.return_value = resp # The retry returns 401 again
    
    # 1st Call: Should retry
    res1 = auth.handle_401(resp)
    assert resp.connection.send.call_count == 1
    
    # 2nd Call: Processing the result of the first retry (which was 401)
    # The internal counter should now prevent another retry
    res2 = auth.handle_401(res1)
    
    # Should NOT retry again (count remains 1)
    assert resp.connection.send.call_count == 1
    # Should return the response unmodified
    assert res2 == res1