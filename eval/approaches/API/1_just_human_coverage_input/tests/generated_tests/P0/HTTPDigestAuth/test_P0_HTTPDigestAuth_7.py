import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest

def test_http_digest_auth_preemptive():
    """
    Test that if a nonce was successfully established in a previous request (pre-emptive auth),
    the Authorization header is added immediately when auth is called, without waiting for a 401.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Manually initialize state to simulate a prior successful handshake
    auth.init_per_thread_state()
    auth._thread_local.last_nonce = "cached_nonce"
    auth._thread_local.chal = {
        "realm": "cached_realm",
        "nonce": "cached_nonce",
        "algorithm": "MD5",
        "qop": "auth"
    }
    auth._thread_local.nonce_count = 1
    
    req = PreparedRequest()
    req.method = "GET"
    req.url = "http://example.org/"
    req.headers = {}
    req.hooks = {"response": []}
    
    # Applying auth should now add header immediately
    auth(req)
    
    auth_header = req.headers.get("Authorization")
    assert auth_header is not None
    assert 'Digest' in auth_header
    assert 'nonce="cached_nonce"' in auth_header
    assert 'realm="cached_realm"' in auth_header