from requests.sessions import SessionRedirectMixin
from requests.models import Request, Response

class MockSession(SessionRedirectMixin):
    def __init__(self):
        self.trust_env = False

def test_rebuild_auth_4():
    # Test no auth to strip
    session = MockSession()
    
    req = Request("GET", "http://new-host.com").prepare()
    # No Auth header
    
    resp = Response()
    resp.request = Request("GET", "http://old-host.com").prepare()
    
    session.rebuild_auth(req, resp)
    
    assert "Authorization" not in req.headers
