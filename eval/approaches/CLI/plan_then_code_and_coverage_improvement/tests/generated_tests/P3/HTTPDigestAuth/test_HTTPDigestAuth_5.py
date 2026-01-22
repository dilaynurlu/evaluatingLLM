from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_HTTPDigestAuth_5():
    # Verify hooks registration in __call__
    auth = HTTPDigestAuth("u", "p")
    r = Request(method="GET", url="http://example.com/").prepare()
    
    # __call__ modifies the request object (PreparedRequest usually, or Request?)
    # The signature is __call__(self, r).
    # It registers hooks.
    
    auth(r)
    
    assert "response" in r.hooks
    assert auth.handle_401 in r.hooks["response"]
    assert auth.handle_redirect in r.hooks["response"]