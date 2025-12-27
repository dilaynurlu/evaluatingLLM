import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth

def test_handle_401_unsupported_qop():
    """
    Test that if qop is provided but not 'auth' (and not empty), 
    build_digest_header returns None and Authorization header is set to None.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    response_401 = Mock()
    response_401.status_code = 401
    # 'auth-int' is not supported by requests HTTPDigestAuth currently
    response_401.headers = {
        "www-authenticate": 'Digest realm="r", nonce="n", qop="auth-int"'
    }
    
    request = Mock()
    request.headers = {}
    request.copy.return_value = Mock(headers={}, method="GET", url="http://a.com")
    response_401.request = request
    response_401.connection.send.return_value = Mock(history=[])
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth(request)
        auth.handle_401(response_401)
        
    retry_req = response_401.connection.send.call_args[0][0]
    # Check result of logic: else: return None -> header = None
    assert retry_req.headers.get("Authorization") is None