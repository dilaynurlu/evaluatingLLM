import pytest
import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_http_digest_auth_no_qop():
    """
    Test Digest Authentication for legacy servers that provide no 'qop' field.
    The resulting header should NOT contain qop, nc, or cnonce.
    """
    auth = HTTPDigestAuth("user", "pass")
    url = "http://example.org/dir/index.html"
    req = requests.Request("GET", url).prepare()
    
    resp = requests.Response()
    resp.status_code = 401
    resp.url = url
    resp.request = req
    # Challenge without qop
    resp.headers = {
        "www-authenticate": 'Digest realm="LegacyRealm", nonce="legacyNonce"'
    }
    resp._content = b""
    
    resp.connection = Mock()
    resp.raw = Mock()
    resp.connection.send.return_value = requests.Response()
    
    auth(req)
    auth.handle_401(resp)
    
    sent_req = resp.connection.send.call_args[0][0]
    auth_header = sent_req.headers["Authorization"]
    
    assert 'username="user"' in auth_header
    assert 'realm="LegacyRealm"' in auth_header
    assert 'nonce="legacyNonce"' in auth_header
    assert 'uri="/dir/index.html"' in auth_header
    assert 'response="' in auth_header
    
    # Assert missing fields for legacy mode
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header