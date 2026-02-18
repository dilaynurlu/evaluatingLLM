import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_HTTPDigestAuth_call_hooks():
    auth = HTTPDigestAuth("user", "pass")
    r = Response()
    r.request = Request()
    # mock register_hook
    hooks = {}
    def register_hook(event, hook):
        hooks.setdefault(event, []).append(hook)
    r.register_hook = register_hook
    
    auth(r)
    
    assert auth.handle_401 in hooks["response"]
    assert auth.handle_redirect in hooks["response"]
