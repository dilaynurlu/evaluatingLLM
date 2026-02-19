import pytest
import re
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_nonce_increment():
    """
    Test that reusing the same nonce increments the nonce count (nc).
    Refined to test the sequence naturally without modifying private attributes.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # --- Request 1 ---
    req1 = Request("GET", "http://example.com/").prepare()
    auth(req1)
    
    resp1 = Response()
    resp1.status_code = 401
    resp1.request = req1
    resp1.headers = CaseInsensitiveDict({
        "www-authenticate": 'Digest realm="testrealm", nonce="repeated_nonce", qop="auth"'
    })
    resp1.raw = Mock()
    resp1._content = b""
    resp1.connection = Mock()
    resp1.connection.send.return_value = Response() # Success for first retry
    
    # Handle first 401
    auth.handle_401(resp1)
    
    req1_retry = resp1.connection.send.call_args[0][0]
    auth_header1 = req1_retry.headers["Authorization"]
    assert "nc=00000001" in auth_header1
    
    # --- Request 2 (Sequence implies reuse of Auth object state) ---
    req2 = Request("GET", "http://example.com/").prepare()
    auth(req2)
    
    resp2 = Response()
    resp2.status_code = 401
    resp2.request = req2
    resp2.headers = CaseInsensitiveDict({
        "www-authenticate": 'Digest realm="testrealm", nonce="repeated_nonce", qop="auth"'
    })
    resp2.raw = Mock()
    resp2._content = b""
    resp2.connection = Mock()
    resp2.connection.send.return_value = Response()
    
    # Handle second 401 with same nonce
    auth.handle_401(resp2)
    
    req2_retry = resp2.connection.send.call_args[0][0]
    auth_header2 = req2_retry.headers["Authorization"]
    
    # Verify nc incremented to 2
    assert "nc=00000002" in auth_header2