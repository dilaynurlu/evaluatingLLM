from requests.auth import HTTPDigestAuth
from requests.models import PreparedRequest

def test_HTTPDigestAuth_call():
    auth = HTTPDigestAuth("user", "pass")
    req = PreparedRequest()
    req.prepare_url("http://example.com", {})
    req.prepare_method("GET")
    req.body = None
    
    auth(req)
    
    assert hasattr(req, "hooks")
    assert auth.handle_401 in req.hooks["response"]
    assert auth.handle_redirect in req.hooks["response"]
    assert hasattr(auth._thread_local, "init")
