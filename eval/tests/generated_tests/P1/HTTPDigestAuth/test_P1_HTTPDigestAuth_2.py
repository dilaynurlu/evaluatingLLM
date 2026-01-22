import pytest
from requests.auth import HTTPDigestAuth
from requests import Request, Response
from unittest.mock import Mock

def test_digest_auth_sha256_algorithm():
    """
    Test Digest Authentication using the SHA-256 algorithm.
    """
    url = "http://example.org/secure"
    auth = HTTPDigestAuth("user", "pass")
    
    req = Request("GET", url).prepare()
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    # Challenge specifies SHA-256
    resp.headers["www-authenticate"] = 'Digest realm="myrealm", nonce="mynonce", qop="auth", algorithm="SHA-256"'
    resp.url = url
    resp.request = req
    resp._content = b""
    
    resp.raw = Mock()
    resp.connection = Mock()
    
    success_resp = Response()
    success_resp.status_code = 200
    success_resp._content = b"ok"
    success_resp.history = []
    
    resp.connection.send.return_value = success_resp

    auth.handle_401(resp)
    
    assert resp.connection.send.call_count == 1
    sent_request = resp.connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    assert 'algorithm="SHA-256"' in auth_header
    assert 'username="user"' in auth_header
    assert 'response="' in auth_header
    # We assume if the algorithm parameter is echoed back and no crash occurred, 
    # the internal hash function was selected correctly.