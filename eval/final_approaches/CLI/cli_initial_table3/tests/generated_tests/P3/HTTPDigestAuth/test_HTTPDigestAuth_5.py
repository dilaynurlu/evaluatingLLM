import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response, Request

def test_HTTPDigestAuth_SHA():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce", qop="auth", algorithm="SHA"'
    r.url = "http://example.com/"
    from requests.sessions import Session
    s = Session()
    req = Request("GET", "http://example.com/")
    r.request = s.prepare_request(req)
    
    class MockConnection:
        def send(self, request, **kwargs):
            resp = Response()
            resp.status_code = 200
            resp.request = request
            resp.history = []
            return resp
            
    r.connection = MockConnection()
    
    new_resp = auth.handle_401(r)
    
    assert new_resp.status_code == 200
    assert "Authorization" in new_resp.request.headers
    assert "algorithm=\"SHA\"" in new_resp.request.headers["Authorization"]