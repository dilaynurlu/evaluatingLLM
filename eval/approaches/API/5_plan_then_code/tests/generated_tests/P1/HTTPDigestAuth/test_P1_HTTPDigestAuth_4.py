import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest

def test_digest_auth_preemptive_cache():
    """
    Test preemptive Digest Auth using cached thread-local state.
    Verifies that if a nonce was previously received (cached), the Authorization
    header is added immediately to the request without waiting for a 401.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Initialize thread local state manually to simulate a previous handshake
    auth.init_per_thread_state()
    auth._thread_local.chal = {
        "realm": "cached-realm",
        "nonce": "cached-nonce",
        "qop": "auth"
    }
    auth._thread_local.last_nonce = "cached-nonce"
    auth._thread_local.nonce_count = 5
    
    # Create a new request
    request = PreparedRequest()
    request.prepare(method="GET", url="http://example.com/api")
    
    # Calling auth(request) should trigger build_digest_header immediately
    auth(request)
    
    assert "Authorization" in request.headers
    auth_header = request.headers["Authorization"]
    
    assert 'Digest ' in auth_header
    assert 'username="user"' in auth_header
    assert 'realm="cached-realm"' in auth_header
    assert 'nonce="cached-nonce"' in auth_header
    
    # Verify nonce count was incremented (logic: if nonce == last_nonce, count += 1)
    # The stored count was 5. Logic increments it.
    # Actually logic in build_digest_header:
    # if nonce == self._thread_local.last_nonce: self._thread_local.nonce_count += 1
    # Check that nc is 6 (format is 8 chars hex: 00000006)
    assert 'nc=00000006' in auth_header