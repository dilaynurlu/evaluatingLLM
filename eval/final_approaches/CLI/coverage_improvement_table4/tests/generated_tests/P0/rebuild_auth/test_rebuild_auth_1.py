from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = False

def test_rebuild_auth_1():
    # Test stripping auth on host change
    session = MockSession()
    
    req = Request("GET", "http://new-host.com").prepare()
    req.headers["Authorization"] = "Basic original"
    
    resp = Response()
    resp.request = Request("GET", "http://old-host.com").prepare()
    
    session.rebuild_auth(req, resp)
    
    assert "Authorization" not in req.headers
