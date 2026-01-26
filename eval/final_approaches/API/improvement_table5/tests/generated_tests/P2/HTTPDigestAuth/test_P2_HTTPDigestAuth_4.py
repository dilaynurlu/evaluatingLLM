import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_no_qop():
    """
    Test Digest Auth when 'qop' is missing in the challenge (RFC 2069 compatibility).
    Should NOT include 'qop', 'nc', or 'cnonce' in the authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    # Challenge without qop
    resp.headers["www-authenticate"] = (
        'Digest realm="oldrealm", nonce="oldnonce"'
    )
    resp._content = b""
    
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    handle_401_hook = req.hooks["response"][0]
    handle_401_hook(resp)
    
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    # In legacy mode (no qop), these fields should strictly be absent
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header
    assert 'response="' in auth_header
    assert 'nonce="oldnonce"' in auth_header