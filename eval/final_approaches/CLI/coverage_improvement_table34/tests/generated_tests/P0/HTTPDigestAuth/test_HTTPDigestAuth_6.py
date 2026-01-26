from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_6():
    # Test handle_401 with no digest header
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Basic realm="foo"'
    
    new_r = auth.handle_401(r)
    
    # Should return original response
    assert new_r is r
    # Should set num_401_calls to 1
    assert auth._thread_local.num_401_calls == 1
