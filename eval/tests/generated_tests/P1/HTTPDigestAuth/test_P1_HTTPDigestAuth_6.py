import pytest
from requests.auth import HTTPDigestAuth
from requests import Request, Response
from unittest.mock import Mock

def test_digest_auth_preemptive_nonce_reuse():
    """
    Test that if a valid nonce is established in the thread-local state,
    subsequent requests reuse it and increment the nonce count (nc),
    adding the Authorization header preemptively (before receiving 401).
    """
    url = "http://example.org/api"
    auth = HTTPDigestAuth("user", "pass")
    
    # --- Request 1: Establish the nonce ---
    req1 = Request("GET", url).prepare()
    auth(req1)
    
    resp1 = Response()
    resp1.status_code = 401
    resp1.headers["www-authenticate"] = 'Digest realm="realm", nonce="persistent_nonce", qop="auth"'
    resp1.url = url
    resp1.request = req1
    resp1._content = b""
    resp1.raw = Mock()
    resp1.connection = Mock()
    
    success_resp = Response()
    success_resp.status_code = 200
    success_resp.history = []
    success_resp._content = b""
    resp1.connection.send.return_value = success_resp
    
    # Handle the first 401. This should set self._thread_local.last_nonce = "persistent_nonce"
    # and use nc=1.
    auth.handle_401(resp1)
    
    # Verify first retry header
    sent_req1 = resp1.connection.send.call_args[0][0]
    auth_val1 = sent_req1.headers["Authorization"]
    assert 'nonce="persistent_nonce"' in auth_val1
    assert 'nc=00000001' in auth_val1
    
    # --- Request 2: Reuse the nonce ---
    req2 = Request("GET", url).prepare()
    
    # Calling auth(req2) should detect existing state and apply header immediately
    auth(req2)
    
    # Verify header is present on req2 without any 401 happening yet
    auth_val2 = req2.headers.get("Authorization")
    assert auth_val2 is not None
    assert 'nonce="persistent_nonce"' in auth_val2
    
    # Verify nonce count incremented
    # Hex value of 2 is 00000002
    assert 'nc=00000002' in auth_val2