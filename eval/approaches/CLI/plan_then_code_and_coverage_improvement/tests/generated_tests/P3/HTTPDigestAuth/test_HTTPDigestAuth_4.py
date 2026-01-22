from requests.auth import HTTPDigestAuth
from requests.models import Response, Request

def test_HTTPDigestAuth_4():
    # handle_401
    # Needs a response with 401 and www-authenticate header
    auth = HTTPDigestAuth("user", "pass")
    
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Digest realm="me@kennethreitz.com", nonce="e30533031024505315354", qop="auth", algorithm="MD5"'
    r.request = Request(method="GET", url="http://example.com/").prepare()
    # We need to mock connection.send or similar to prevent real network call?
    # handle_401 calls r.connection.send(prep, ...)
    # So we must mock r.connection
    
    class MockConnection:
        def send(self, request, **kwargs):
            resp = Response()
            resp.status_code = 200
            resp.request = request
            resp.history = [] # Initialize history
            return resp
            
    r.connection = MockConnection()
    # Also r.content calls r.raw.read... we can mock r.raw or just set r._content
    r._content = b""
    
    # auth() registers hooks.
    # But we can call handle_401 directly if we set up thread state?
    # handle_401 checks self._thread_local.num_401_calls
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    new_r = auth.handle_401(r)
    
    assert new_r.status_code == 200
    assert "Authorization" in new_r.request.headers
    assert new_r.request.headers["Authorization"].startswith("Digest ")