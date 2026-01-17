from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from unittest.mock import Mock

def test_http_digest_auth_init_call():
    auth = HTTPDigestAuth("user", "pass")
    r = PreparedRequest()
    # __call__ registers hooks
    auth(r)
    assert auth.handle_401 in r.hooks["response"]
    assert auth.handle_redirect in r.hooks["response"]
