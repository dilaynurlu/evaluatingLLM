from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from unittest.mock import Mock

def test_http_digest_auth_eq():
    auth1 = HTTPDigestAuth("user", "pass")
    auth2 = HTTPDigestAuth("user", "pass")
    auth3 = HTTPDigestAuth("other", "pass")
    
    assert auth1 == auth2
    assert auth1 != auth3
