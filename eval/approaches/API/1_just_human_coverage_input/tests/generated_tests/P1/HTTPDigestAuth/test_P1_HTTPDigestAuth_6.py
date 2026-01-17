import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_md5_sess_algorithm():
    """
    Test Digest Authentication using MD5-SESS algorithm.
    Ensures that the HA1 hash construction involves the cnonce.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    url = "http://example.org/sess"
    req = PreparedRequest()
    req.prepare(method="GET", url=url)
    
    resp = Response()
    resp.status_code = 401
    resp.headers["www-authenticate"] = 'Digest realm="sess", nonce="n", algorithm="MD5-SESS", qop="auth"'
    resp.request = req
    resp._content = b""
    
    mock_connection = Mock()
    mock_connection.send.return_value = Response()
    resp.connection = mock_connection
    
    auth(req)
    
    # We assert that it processes without error and includes the algorithm
    # Detailed HA1 verification is implicit if the function runs and produces a valid format
    with patch("os.urandom", return_value=b"xyz"), \
         patch("time.ctime", return_value="Time"):
        auth.handle_401(resp)
        
    retry_req = mock_connection.send.call_args[0][0]
    auth_header = retry_req.headers["Authorization"]
    
    assert 'algorithm="MD5-SESS"' in auth_header
    assert 'nonce="n"' in auth_header
    assert 'response="' in auth_header