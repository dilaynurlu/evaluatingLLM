from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_7():
    # Test handle_401 limit reached
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    # Simulate already tried once
    auth._thread_local.num_401_calls = 2
    
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Digest realm="foo", nonce="bar"'
    
    new_r = auth.handle_401(r)
    
    # Should not retry
    assert new_r is r
    # num_401_calls should reset to 1
    assert auth._thread_local.num_401_calls == 1
