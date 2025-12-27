import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_no_qop():
    """
    Test that HTTPDigestAuth handles challenges without a 'qop' field.
    This corresponds to older RFC 2069 behavior where 'nc' and 'cnonce' 
    are not included in the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    request = Mock(spec=requests.PreparedRequest)
    request.method = "GET"
    request.url = "http://example.org/noqop"
    request.headers = {}
    request.body = None
    request._cookies = requests.cookies.RequestsCookieJar()
    request.copy.return_value = request
    request.prepare_cookies = Mock()

    auth(request)

    # Challenge without qop
    response = Mock(spec=requests.Response)
    response.status_code = 401
    response.request = request
    response.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="nonce_val"'
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
    auth.handle_401(response)
    
    # Assert
    auth_header = request.headers["Authorization"]
    assert 'qop=' not in auth_header
    assert 'nc=' not in auth_header
    assert 'cnonce=' not in auth_header
    assert 'response="' in auth_header