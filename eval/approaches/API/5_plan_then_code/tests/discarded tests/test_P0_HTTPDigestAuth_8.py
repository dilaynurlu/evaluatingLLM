import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_ignore_non_401():
    """
    Test that handle_401 does nothing if the status code is not 401.
    It should return the response unchanged and not trigger any new request.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com/").prepare()
    auth(req)
    
    # Create a 403 Forbidden response (not 401)
    resp = Response()
    resp.request = req
    resp.status_code = 403
    resp.headers["www-authenticate"] = 'Digest realm="r", nonce="n"'
    resp._content = b"forbidden"
    resp.raw = Mock()
    
    resp.connection = Mock() # Should not be used
    
    result = auth.handle_401(resp)
    
    # Should return original response object
    assert result is resp
    # connection.send should NOT be called
    assert not resp.connection.send.called
    assert not resp.connection.mock_calls