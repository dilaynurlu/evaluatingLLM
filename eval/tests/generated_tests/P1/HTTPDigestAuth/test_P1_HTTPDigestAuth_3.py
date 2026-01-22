import pytest
from requests.auth import HTTPDigestAuth
from requests import Request, Response
from unittest.mock import Mock

def test_digest_auth_no_qop_legacy():
    """
    Test Digest Authentication when 'qop' is missing from the challenge (RFC 2069 compatibility).
    In this mode, 'cnonce' and 'nc' (nonce count) should NOT be included in the Authorization header.
    """
    url = "http://example.org/legacy"
    auth = HTTPDigestAuth("user", "pass")
    
    req = Request("GET", url).prepare()
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    # No qop parameter
    resp.headers["www-authenticate"] = 'Digest realm="myrealm", nonce="mynonce"'
    resp.url = url
    resp.request = req
    resp._content = b""
    
    resp.raw = Mock()
    resp.connection = Mock()
    
    success_resp = Response()
    success_resp.status_code = 200
    success_resp.history = []
    resp.connection.send.return_value = success_resp

    auth.handle_401(resp)
    
    sent_request = resp.connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    # Assertions for legacy mode
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header
    assert 'response="' in auth_header
    assert 'nonce="mynonce"' in auth_header