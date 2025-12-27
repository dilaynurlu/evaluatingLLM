import requests
from requests.auth import HTTPDigestAuth
from unittest.mock import Mock

def test_digest_auth_sha256_algorithm():
    """
    Test that HTTPDigestAuth correctly handles the 'SHA-256' algorithm
    when provided in the WWW-Authenticate header.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock the initial PreparedRequest
    request = Mock(spec=requests.PreparedRequest)
    request.method = "GET"
    request.url = "http://example.org/resource"
    request.headers = {}
    request.body = None
    request._cookies = requests.cookies.RequestsCookieJar()
    request.copy.return_value = request
    request.prepare_cookies = Mock()

    # Initialize per-thread state by calling the auth object
    auth(request)

    # Mock the 401 Response containing the challenge
    response = Mock(spec=requests.Response)
    response.status_code = 401
    response.request = request
    response.headers = {
        "www-authenticate": 'Digest realm="myrealm", nonce="nonce_val", algorithm="SHA-256", qop="auth"'
    }
    response.is_redirect = False
    response.content = b""
    response.raw = Mock()
    
    # Mock the connection to simulate the retry sending a success response
    retry_response = Mock(spec=requests.Response)
    retry_response.status_code = 200
    retry_response.history = []
    retry_response.request = request
    
    response.connection = Mock()
    response.connection.send.return_value = retry_response
    
    # Act: Handle the 401
    result = auth.handle_401(response)
    
    # Assert
    assert result.status_code == 200
    assert "Authorization" in request.headers
    auth_header = request.headers["Authorization"]
    
    # Verify header construction
    assert auth_header.startswith("Digest ")
    assert 'algorithm="SHA-256"' in auth_header
    assert 'username="user"' in auth_header
    assert 'nonce="nonce_val"' in auth_header
    assert 'response="' in auth_header