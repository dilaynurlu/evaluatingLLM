from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from unittest.mock import Mock

def test_http_digest_auth_retry_limit():
    auth = HTTPDigestAuth("user", "pass")
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce"'
    r.request = PreparedRequest()
    
    auth(r.request)
    auth._thread_local.num_401_calls = 2 # Max retries reached
    
    result = auth.handle_401(r)
    # Should not retry
    assert result is r
    # num_401_calls should reset to 1
    assert auth._thread_local.num_401_calls == 1
