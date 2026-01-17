import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_nonce_counting():
    """
    Test that the nonce count (nc) increments when the server returns the same nonce 
    in subsequent 401 responses, and is formatted as an 8-digit hexadecimal string.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com/").prepare()
    auth(req) # Init state
    
    nonce = "repeated_nonce"
    
    # First 401 response
    resp1 = Response()
    resp1.request = req
    resp1.status_code = 401
    resp1.headers["www-authenticate"] = f'Digest realm="r", nonce="{nonce}", qop="auth"'
    resp1._content = b""
    resp1.raw = Mock()
    resp1.connection = Mock()
    resp1.connection.send.return_value = Response()

    with patch("requests.auth.os.urandom", return_value=b"x"), patch("requests.auth.time.ctime", return_value="t"):
        # Handle first 401
        auth.handle_401(resp1)
        
        args1, _ = resp1.connection.send.call_args
        header1 = args1[0].headers["Authorization"]
        assert "nc=00000001" in header1

        # Second 401 response (same nonce)
        # Note: We simulate a new response object for the retry or subsequent request
        # but sharing the same Auth instance state.
        resp2 = Response()
        resp2.request = req
        resp2.status_code = 401
        resp2.headers["www-authenticate"] = f'Digest realm="r", nonce="{nonce}", qop="auth"'
        resp2._content = b""
        resp2.raw = Mock()
        resp2.connection = Mock()
        resp2.connection.send.return_value = Response()

        # Handle second 401
        auth.handle_401(resp2)
        
        args2, _ = resp2.connection.send.call_args
        header2 = args2[0].headers["Authorization"]
        # Verify nc incremented
        assert "nc=00000002" in header2