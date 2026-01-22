from requests.auth import HTTPDigestAuth
from requests.models import Response, Request

def test_HTTPDigestAuth_3():
    # Test handle_401 with digest challenge
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce", qop="auth"'
    r.request = Request(method="GET", url="http://example.com").prepare()
    # Mocking history to avoid infinite loops if it were real logic, 
    # but here we just check if it returns a new response (the retried request).
    
    # We need to mock connection.send because handle_401 calls it.
    # But for a unit test without mocks, we might crash or need a real connection.
    # The prompt allows "Mock only external side effects when necessary".
    # Connection sending is definitely an external side effect.
    
    class MockConnection:
        def send(self, request, **kwargs):
            resp = Response()
            resp.status_code = 200
            resp.request = request
            resp.history = []
            return resp
    
    r.connection = MockConnection()
    r.raw = None # To avoid seek issues or need to mock it better if content consumption happens
    
    # handle_401 calls r.content then r.close(). 
    # r.content property reads from r.raw.
    # Let's mock r.content to be safe/easy.
    r._content = b""
    
    # Simulate prior call to __call__
    auth._thread_local.num_401_calls = 1

    # Call handle_401
    new_r = auth.handle_401(r)
    
    assert new_r.status_code == 200
    assert auth._thread_local.num_401_calls == 2
    assert auth._thread_local.chal["realm"] == "realm"
