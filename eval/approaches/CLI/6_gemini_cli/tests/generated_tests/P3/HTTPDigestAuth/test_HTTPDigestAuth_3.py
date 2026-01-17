from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_http_digest_auth_handle_401_sha256():
    auth = HTTPDigestAuth("user", "pass")
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce", algorithm="SHA-256", qop="auth"'
    r.request = PreparedRequest()
    r.request.url = "http://example.com/"
    r.request.method = "GET"
    r.request.headers = {}
    r.request._cookies = RequestsCookieJar()
    r.connection = Mock()
    r.connection.send.return_value = Response()
    r.raw = Mock()
    r.raw.stream.return_value = iter([b""])
    r.raw._original_response = None

    auth(r.request)
    auth.handle_401(r)
    
    args, _ = r.connection.send.call_args
    sent_request = args[0]
    # Check if algorithm is SHA-256 in header (it might not be explicitly present if default, but here it is)
    # Actually requests adds algorithm="..." if it was in challenge
    assert 'algorithm="SHA-256"' in sent_request.headers["Authorization"]
