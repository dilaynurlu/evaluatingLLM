import pytest
from unittest.mock import MagicMock, patch
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_handle_401_basic_flow():
    """
    Test the standard flow where a 401 response with Digest challenge
    results in a new request with the correct Authorization header using MD5 (default).
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Mock the initial PreparedRequest passed to __call__
    initial_request = MagicMock(spec=requests.PreparedRequest)
    initial_request.method = "GET"
    initial_request.url = "http://example.org/"
    initial_request.headers = {}
    initial_request.body = None # No body to seek
    initial_request.register_hook = MagicMock()
    
    # Initialize state
    auth(initial_request)
    
    # Mock the 401 Response object
    r_401 = MagicMock(spec=requests.Response)
    r_401.request = initial_request
    # Mock copy to return a new mock we can inspect
    new_request = MagicMock(spec=requests.PreparedRequest)
    new_request.headers = {}
    new_request.method = "GET"
    new_request.url = "http://example.org/"
    new_request._cookies = MagicMock()
    # Ensure prepare_cookies is mocked
    new_request.prepare_cookies = MagicMock()
    
    initial_request.copy.return_value = new_request
    
    r_401.headers = {
        "www-authenticate": 'Digest realm="testrealm", nonce="testnonce", qop="auth", opaque="testopaque"'
    }
    r_401.status_code = 401
    r_401.is_redirect = False
    r_401.content = b""
    r_401.raw = MagicMock()
    
    # Connection mock to return a 200 OK on the second try
    r_success = MagicMock(spec=requests.Response)
    r_success.status_code = 200
    r_success.history = []
    
    r_401.connection = MagicMock()
    r_401.connection.send.return_value = r_success
    
    # Patch internals to ensure determinism and isolation
    with patch("requests.auth.time") as mock_time, \
         patch("requests.auth.os") as mock_os, \
         patch("requests.auth.extract_cookies_to_jar"):
        
        mock_time.ctime.return_value = "Mon Jan 01 00:00:00 2000"
        mock_os.urandom.return_value = b"\x00" * 8
        
        # Execute
        result = auth.handle_401(r_401)
        
        # Assertions
        assert result == r_success
        assert r_401.connection.send.called
        
        # Verify Authorization Header
        auth_header = new_request.headers.get("Authorization")
        assert auth_header is not None
        assert auth_header.startswith("Digest ")
        
        # Check components
        parts = {
            k.strip(): v.strip('"') 
            for k, v in [x.split("=", 1) for x in auth_header[7:].split(",")]
        }
        
        assert parts["username"] == "user"
        assert parts["realm"] == "testrealm"
        assert parts["nonce"] == "testnonce"
        assert parts["uri"] == "/"
        assert parts["qop"] == "auth"
        assert parts["opaque"] == "testopaque"
        assert "response" in parts
        assert "cnonce" in parts
        assert "nc" in parts