import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_query_params():
    """
    Test that the 'uri' directive in the Authorization header correctly preserves
    query parameters from the request URL.
    """
    auth = HTTPDigestAuth("user", "pass")
    url = "http://example.com/search?q=foo&page=1"
    req = Request("GET", url).prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.request = req
    response.url = url
    response._content = b""
    response.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth"'
    
    response.connection = Mock()
    response.connection.send.return_value = Response()
    
    auth.handle_401(response)
    
    sent_req = response.connection.send.call_args[0][0]
    auth_header = sent_req.headers["Authorization"]
    
    parts = auth_header[7:].split(", ")
    header_dict = {k: v.strip('"') for k, v in [p.split("=", 1) for p in parts]}
    
    expected_uri = "/search?q=foo&page=1"
    assert header_dict['uri'] == expected_uri