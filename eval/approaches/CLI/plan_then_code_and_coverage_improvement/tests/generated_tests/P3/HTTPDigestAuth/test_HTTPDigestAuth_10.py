from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_10():
    # handle_redirect: resets num_401_calls
    auth = HTTPDigestAuth("u", "p")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 5
    
    r = Response()
    r.status_code = 301 # is_redirect property relies on status code
    r.headers["Location"] = "new"
    
    auth.handle_redirect(r)
    
    assert auth._thread_local.num_401_calls == 1
