from requests.auth import HTTPDigestAuth
from requests.models import Response, PreparedRequest
from requests.cookies import RequestsCookieJar
from unittest.mock import Mock

def test_http_digest_auth_handle_401_md5():
    auth = HTTPDigestAuth("user", "pass")
    r = Response()
    r.status_code = 401
    r.headers["www-authenticate"] = 'Digest realm="realm", nonce="nonce", algorithm="MD5", qop="auth"'
    r.request = PreparedRequest()
    r.request.url = "http://example.com/"
    r.request.method = "GET"
    r.request.headers = {}
    r.request._cookies = RequestsCookieJar()
    r.connection = Mock()
    r.connection.send.return_value = Response()
    r.raw = Mock() # for extract_cookies_to_jar
    r.raw.stream.return_value = iter([b""])
    r.raw._original_response = None

    # First call initializes state
    auth(r.request)
    
    # Trigger handle_401
    new_r = auth.handle_401(r)
    
    assert r.connection.send.called
    args, _ = r.connection.send.call_args
    sent_request = args[0]
    assert "Authorization" in sent_request.headers
    assert "Digest" in sent_request.headers["Authorization"]
    assert 'algorithm="MD5"' in sent_request.headers["Authorization"]
