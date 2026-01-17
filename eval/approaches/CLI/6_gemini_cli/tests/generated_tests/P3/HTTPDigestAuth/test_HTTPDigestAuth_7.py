from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest

def test_http_digest_auth_ignore_non_4xx():
    auth = HTTPDigestAuth("user", "pass")
    r = Response()
    r.status_code = 200
    r.request = PreparedRequest()
    
    auth(r.request)
    result = auth.handle_401(r)
    # Should return original response without doing anything
    assert result is r
    assert auth._thread_local.num_401_calls == 1
