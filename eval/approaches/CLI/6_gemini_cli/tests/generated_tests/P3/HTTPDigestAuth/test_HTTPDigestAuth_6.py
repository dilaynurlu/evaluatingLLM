from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_http_digest_auth_handle_redirect():
    auth = HTTPDigestAuth("user", "pass")
    r = Response()
    r.request = PreparedRequest()
    auth(r.request)
    
    # Set num_401_calls to something high
    auth._thread_local.num_401_calls = 5
    
    # Mock redirect
    # r.is_redirect is a property, so we set status code and location
    r.status_code = 302 
    r.headers["Location"] = "http://example.com/new"
    
    auth.handle_redirect(r)
    assert auth._thread_local.num_401_calls == 1
