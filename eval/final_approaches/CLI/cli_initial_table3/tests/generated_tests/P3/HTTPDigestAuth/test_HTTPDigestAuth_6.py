import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response, Request

def test_HTTPDigestAuth_stop_recursion():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 2
    
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce", qop="auth"'
    r.url = "http://example.com/"
    r.request = Request("GET", "http://example.com/")
    
    # It should just return the response without retrying
    new_resp = auth.handle_401(r)
    
    assert new_resp == r
    assert new_resp.status_code == 401
