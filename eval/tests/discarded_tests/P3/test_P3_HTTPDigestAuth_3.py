import pytest
from unittest.mock import Mock, MagicMock, patch
from requests.auth import HTTPDigestAuth
from requests import PreparedRequest

def test_digest_auth_handle_401_sha256_sess():
    """
    Test handling of a 401 response with SHA-256-sess algorithm.
    Verifies that the algorithm is respected and cnonce is generated.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    initial_request = PreparedRequest()
    initial_request.prepare(method="GET", url="http://example.org/secure")
    
    response = Mock()
    response.status_code = 401
    response.headers = {
        "www-authenticate": 'Digest realm="realm2", nonce="nonceSHA", qop="auth", algorithm="SHA-256-sess"'
    }
    response.is_redirect = False
    response.request = initial_request
    response.content = b""
    response.connection = Mock()
    response.connection.send.return_value = Mock(history=[])
    
    # Init auth
    auth(initial_request)
    
    with patch("requests.auth.extract_cookies_to_jar"):
        auth.handle_401(response)
        
        assert response.connection.send.called
        sent_req = response.connection.send.call_args[0][0]
        auth_header = sent_req.headers.get("Authorization", "")
        
        # Verify algorithm and presence of cnonce (client nonce) required for -sess
        assert 'algorithm="SHA-256-sess"' in auth_header
        assert 'nonce="nonceSHA"' in auth_header
        assert 'cnonce="' in auth_header
        assert 'nc=00000001' in auth_header

'''
Execution failed:

 # Verify algorithm and presence of cnonce (client nonce) required for -sess
>           assert 'algorithm="SHA-256-sess"' in auth_header
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           TypeError: argument of type 'NoneType' is not iterable

eval/tests/generated_tests/P3/HTTPDigestAuth/test_P3_HTTPDigestAuth_3.py:38: TypeError
'''