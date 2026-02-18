from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = False

def test_rebuild_auth_2():
    # Test keeping auth on same host
    session = MockSession()
    
    req = Request("GET", "http://example.com/new").prepare()
    req.headers["Authorization"] = "Basic original"
    
    resp = Response()
    resp.request = Request("GET", "http://example.com/old").prepare()
    
    session.rebuild_auth(req, resp)
    
    assert req.headers["Authorization"] == "Basic original"
