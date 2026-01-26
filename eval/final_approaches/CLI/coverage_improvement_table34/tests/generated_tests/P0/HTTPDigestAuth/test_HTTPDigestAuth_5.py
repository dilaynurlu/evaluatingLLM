from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_5():
    # Test handle_401 with non-4xx response
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Response()
    r.status_code = 500
    r.headers["www-authenticate"] = 'Digest ...'
    
    new_r = auth.handle_401(r)
    
    # Should return original response without doing anything
    assert new_r is r
    # Should set num_401_calls to 1
    assert auth._thread_local.num_401_calls == 1
