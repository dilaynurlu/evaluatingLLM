import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_opaque_passthrough():
    """
    Test that the 'opaque' directive from the server challenge is passed back
    unmodified in the client's Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com/").prepare()
    auth(req)
    
    resp = Response()
    resp.request = req
    resp.status_code = 401
    opaque_val = "5ccc069c403ebaf9f0171e9517f40e41"
    resp.headers["www-authenticate"] = f'Digest realm="r", nonce="n", opaque="{opaque_val}"'
    resp._content = b""
    resp.raw = Mock()
    
    mock_send = Mock()
    mock_send.return_value = Response()
    resp.connection = Mock()
    resp.connection.send = mock_send

    auth.handle_401(resp)
    
    assert mock_send.called
    auth_header = mock_send.call_args[0][0].headers["Authorization"]
    
    assert f'opaque="{opaque_val}"' in auth_header