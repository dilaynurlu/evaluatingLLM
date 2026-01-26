import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.adapters import HTTPAdapter

def test_digest_auth_preemptive_nonce_reuse():
    """
    Test that HTTPDigestAuth reuses the nonce and increments the nonce count (nc)
    when a subsequent request is made after a successful challenge.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # --- Step 1: Initial Request & Challenge ---
    req1 = PreparedRequest()
    req1.prepare(method="GET", url="http://example.com/1")
    auth(req1)
    
    r_401 = Response()
    r_401.status_code = 401
    r_401.request = req1
    r_401._content = b""
    r_401._content_consumed = True
    nonce = "persistent_nonce"
    r_401.headers["www-authenticate"] = f'Digest realm="r", nonce="{nonce}", qop="auth"'
    
    adapter_mock = Mock(spec=HTTPAdapter)
    r_ok = Response()
    r_ok.status_code = 200
    r_ok._content = b""
    r_ok.history = []
    adapter_mock.send.return_value = r_ok
    r_401.connection = adapter_mock
    
    # Handle first 401, which sets internal state (last_nonce, etc.)
    auth.handle_401(r_401)
    
    # Verify first retry had nc=1
    args1, _ = adapter_mock.send.call_args
    auth_header1 = args1[0].headers["Authorization"]
    assert f'nonce="{nonce}"' in auth_header1
    assert 'nc=00000001' in auth_header1
    
    # --- Step 2: Second Request (Pre-emptive) ---
    req2 = PreparedRequest()
    req2.prepare(method="GET", url="http://example.com/2")
    
    # Calling auth(req2) should immediately attach Authorization header using cached state
    auth(req2)
    
    auth_header2 = req2.headers.get("Authorization")
    assert auth_header2 is not None
    assert auth_header2.startswith("Digest ")
    
    # Verify reuse of nonce and increment of nc
    assert f'nonce="{nonce}"' in auth_header2
    assert 'nc=00000002' in auth_header2