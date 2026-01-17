import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests import Request, Response

def test_digest_auth_opaque_parameter():
    """
    Test that the 'opaque' parameter provided by the server is returned unchanged
    in the client's Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.org/opaque").prepare()
    auth(req)
    
    response = Response()
    response.status_code = 401
    response.url = "http://example.org/opaque"
    response.request = req
    # Challenge with opaque data
    response.headers["www-authenticate"] = (
        'Digest realm="r", nonce="n", qop="auth", opaque="server_state_data"'
    )
    response._content = b""
    response.raw = Mock()
    
    mock_connection = Mock()
    response.connection = mock_connection
    mock_connection.send.return_value = Response()
    
    auth.handle_401(response)
    
    assert mock_connection.send.called
    sent_request = mock_connection.send.call_args[0][0]
    auth_header = sent_request.headers["Authorization"]
    
    assert 'opaque="server_state_data"' in auth_header