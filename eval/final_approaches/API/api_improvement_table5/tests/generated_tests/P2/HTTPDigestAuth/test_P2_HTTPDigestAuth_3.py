import pytest
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response
from unittest.mock import Mock

def test_digest_auth_md5_sess_algorithm():
    """
    Test Digest Auth with algorithm="MD5-SESS".
    Verifies that the code path for HA1 modification in MD5-SESS is executed.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    req = PreparedRequest()
    req.prepare(method="GET", url="http://example.com/")
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers["www-authenticate"] = (
        'Digest realm="sess_realm", nonce="sess_nonce", '
        'qop="auth", algorithm="MD5-SESS"'
    )
    resp._content = b""
    
    mock_connection = Mock()
    resp.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    handle_401_hook = req.hooks["response"][0]
    handle_401_hook(resp)
    
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    assert 'algorithm="MD5-SESS"' in auth_header
    # The response calculation logic involves cnonce for MD5-SESS, 
    # but the external appearance is just a hash. We verify the header is formed.
    assert 'response="' in auth_header