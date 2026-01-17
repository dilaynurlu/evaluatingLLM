import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_opaque():
    """
    Test that the 'opaque' value provided by the server is echoed back verbatim
    in the Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com").prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.request = req
    response.url = "http://example.com"
    response._content = b""
    opaque_val = "5ccc069c403ebaf9f0171e9517f40e41"
    response.headers["www-authenticate"] = f'Digest realm="r", nonce="n", opaque="{opaque_val}"'
    
    response.connection = Mock()
    response.connection.send.return_value = Response()
    
    auth.handle_401(response)
    
    sent_req = response.connection.send.call_args[0][0]
    auth_header = sent_req.headers["Authorization"]
    
    parts = auth_header[7:].split(", ")
    header_dict = {k: v.strip('"') for k, v in [p.split("=", 1) for p in parts]}
    
    assert header_dict['opaque'] == opaque_val