import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_opaque_handling():
    """
    Test that HTTPDigestAuth echoes the 'opaque' directive from the server
    back in the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    request = Mock(spec=requests.PreparedRequest)
    request.method = "GET"
    request.url = "http://example.org/opaque"
    request.headers = {}
    request.body = None
    request._cookies = requests.cookies.RequestsCookieJar()
    request.copy.return_value = request
    request.prepare_cookies = Mock()

    auth(request)

    # Challenge with opaque data
    response = Mock(spec=requests.Response)
    response.status_code = 401
    response.request = request
    response.headers = {
        "www-authenticate": 'Digest realm="realm", nonce="n", qop="auth", opaque="secret_data_XYZ"'
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
    assert 'opaque="secret_data_XYZ"' in auth_header