import pytest
from unittest.mock import Mock, patch
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest, Response

def test_digest_auth_nonce_count_increment():
    """
    Test that reusing the same nonce increments the nonce count (nc).
    This simulates a session where the server accepts the nonce for multiple requests
    or challenges again with the same nonce.
    """
    auth = HTTPDigestAuth("user", "pass")
    nonce = "persistent_nonce"
    
    # --- First Request ---
    req1 = PreparedRequest()
    req1.prepare(method="GET", url="http://example.org/1")
    
    resp1 = Response()
    resp1.status_code = 401
    resp1.headers["www-authenticate"] = f'Digest realm="r", nonce="{nonce}", qop="auth"'
    resp1.request = req1
    resp1._content = b""
    
    conn1 = Mock()
    conn1.send.return_value = Response()
    resp1.connection = conn1
    
    auth(req1) # Initialize
    auth.handle_401(resp1)
    
    header1 = conn1.send.call_args[0][0].headers["Authorization"]
    assert "nc=00000001" in header1
    
    # --- Second Request (Same Auth instance, same thread) ---
    req2 = PreparedRequest()
    req2.prepare(method="GET", url="http://example.org/2")
    
    resp2 = Response()
    resp2.status_code = 401
    # Server sends SAME nonce
    resp2.headers["www-authenticate"] = f'Digest realm="r", nonce="{nonce}", qop="auth"'
    resp2.request = req2
    resp2._content = b""
    
    conn2 = Mock()
    conn2.send.return_value = Response()
    resp2.connection = conn2
    
    # Note: We must call auth(req2) to attach hooks, but it also checks init state.
    # The state (last_nonce) should persist in thread local.
    auth(req2)
    auth.handle_401(resp2)
    
    header2 = conn2.send.call_args[0][0].headers["Authorization"]
    
    # Verify nonce count incremented
    assert "nc=00000002" in header2
    assert f'nonce="{nonce}"' in header2