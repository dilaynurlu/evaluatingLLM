import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_unsupported_algorithm():
    """
    Test that an unsupported algorithm results in no Authorization header being added.
    Refined assertion to check dictionary containment safely.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com/").prepare()
    auth(req)
    
    resp = Response()
    resp.status_code = 401
    resp.request = req
    resp.headers = CaseInsensitiveDict({
        "www-authenticate": 'Digest realm="realm", nonce="nonce", algorithm="UNSUPPORTED-ALG"'
    })
    
    mock_connection = Mock()
    resp.connection = mock_connection
    resp.connection.send.return_value = Response() # Ensure send doesn't crash
    resp.raw = Mock()
    resp._content = b""
    
    auth.handle_401(resp)
    
    assert mock_connection.send.called
    sent_request = mock_connection.send.call_args[0][0]
    
    # Verify Authorization header is strictly missing
    assert "Authorization" not in sent_request.headers