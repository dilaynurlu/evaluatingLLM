import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_md5_sess_algorithm():
    """
    Test that HTTPDigestAuth correctly handles the 'MD5-SESS' algorithm.
    This algorithm triggers a specific hash calculation path for HA1.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock the initial PreparedRequest
    request = Mock(spec=requests.PreparedRequest)
    request.method = "GET"
    request.url = "http://example.org/sess"
    request.headers = {}
    request.body = None
    request._cookies = requests.cookies.RequestsCookieJar()
    request.copy.return_value = request
    request.prepare_cookies = Mock()

    auth(request)

    # Mock the 401 Response with MD5-SESS
    response = Mock(spec=requests.Response)
    response.status_code = 401
    response.request = request
    response.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="nonce_val", algorithm="MD5-SESS", qop="auth"'
    }
    response.is_redirect = False
    response.content = b""
    response.raw = Mock()
    
    retry_response = Mock(spec=requests.Response)
    retry_response.status_code = 200
    retry_response.history = []
    retry_response.request = request
    
    response.connection = Mock()
    response.connection.send.return_value = retry_response
    
    # Act
    result = auth.handle_401(response)
    
    # Assert
    assert result.status_code == 200
    auth_header = request.headers["Authorization"]
    assert 'algorithm="MD5-SESS"' in auth_header
    assert 'response="' in auth_header