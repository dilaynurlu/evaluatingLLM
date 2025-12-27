import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth

def test_handle_401_md5_success():
    """
    Test the standard Digest Auth flow with MD5 algorithm.
    Should generate an Authorization header and retry the request.
    """
    auth = HTTPDigestAuth("myuser", "mypass")
    
    # Setup 401 Response
    response_401 = Mock()
    response_401.status_code = 401
    response_401.headers = {
        "www-authenticate": 'Digest realm="myrealm", nonce="mynonce", opaque="myopaque"'
    }
    response_401.is_redirect = False
    response_401.content = b"content"
    
    # Setup Original Request
    original_req = Mock()
    original_req.url = "http://example.com/path"
    original_req.method = "GET"
    original_req.headers = {}
    original_req.body = None
    original_req._cookies = Mock()
    
    # Mock copy() to return a new request object to be modified
    new_req = Mock()
    new_req.headers = {}
    new_req.method = "GET"
    new_req.url = "http://example.com/path"
    new_req._cookies = Mock()
    original_req.copy.return_value = new_req
    
    response_401.request = original_req
    
    # Mock connection.send() to return the retry response
    retry_response = Mock()
    retry_response.history = []
    retry_response.request = new_req
    response_401.connection.send.return_value = retry_response
    
    # Patch extract_cookies_to_jar as it requires real objects
    with patch("requests.auth.extract_cookies_to_jar"):
        # Initial call to set up thread local state
        auth(original_req)
        
        # Act
        result = auth.handle_401(response_401)
    
    # Assert
    assert result == retry_response
    assert response_401.connection.send.called
    
    # Check Authorization header construction
    auth_header = new_req.headers.get("Authorization")
    assert auth_header is not None
    assert auth_header.startswith("Digest ")
    assert 'username="myuser"' in auth_header
    assert 'realm="myrealm"' in auth_header
    assert 'nonce="mynonce"' in auth_header
    assert 'opaque="myopaque"' in auth_header
    assert 'uri="/path"' in auth_header
    assert 'response="' in auth_header
    # Default algorithm is MD5, usually not explicitly added if not in challenge, 
    # or added if code enforces it. Code adds it if 'algorithm' key is in chal.
    # The challenge didn't have algorithm, so it defaults to MD5 internally but header depends on chal.
    # Code: "if algorithm: base += ..." -> Since challenge had no algorithm, header won't have it.
    assert 'algorithm=' not in auth_header