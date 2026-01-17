import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_http_digest_auth_algorithm_sha256():
    """
    Test Digest Authentication using SHA-256 algorithm.
    """
    auth = HTTPDigestAuth("user", "pass")
    url = "http://example.org/"
    req = requests.Request("GET", url).prepare()
    
    resp = requests.Response()
    resp.status_code = 401
    resp.url = url
    resp.request = req
    resp.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="123", algorithm="SHA-256"'
    }
    resp._content = b""
    
    resp.connection = Mock()
    resp.raw = Mock()
    resp.connection.send.return_value = requests.Response()
    
    auth(req)
    auth.handle_401(resp)
    
    sent_req = resp.connection.send.call_args[0][0]
    auth_header = sent_req.headers["Authorization"]
    
    assert 'algorithm="SHA-256"' in auth_header
    assert 'username="user"' in auth_header