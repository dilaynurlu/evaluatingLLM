import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
from requests.models import Response, Request
from requests.cookies import RequestsCookieJar

def test_HTTPDigestAuth_handle_401_simple():
    """
    Test that handle_401 parses the challenge and retries with Authorization header.
    """
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 1
    
    # Mock Response
    r = MagicMock(spec=Response)
    r.status_code = 401
    r.headers = {
        "www-authenticate": 'Digest realm="testrealm", nonce="testnonce", qop="auth", opaque="testopaque"'
    }
    r.request = MagicMock()
    r.request.headers = {}
    r.request.url = "http://example.com/"
    r.request.method = "GET"
    r.content = b""
    r.connection = MagicMock()
    r.raw = MagicMock()
    
    # Mock the retried response
    retried_response = MagicMock(spec=Response)
    retried_response.status_code = 200
    retried_response.history = []
    r.connection.send.return_value = retried_response
    
    # Prepare the request copy
    prep = MagicMock()
    prep.headers = {}
    prep.url = "http://example.com/"
    prep.method = "GET"
    prep._cookies = RequestsCookieJar()
    r.request.copy.return_value = prep
    
    # Act
    result = auth.handle_401(r)
    
    # Assert
    assert result == retried_response
    assert "Authorization" in prep.headers
    auth_header = prep.headers["Authorization"]
    assert 'username="user"' in auth_header
    assert 'realm="testrealm"' in auth_header
    assert 'nonce="testnonce"' in auth_header
    assert 'uri="/"' in auth_header
    assert 'response="' in auth_header
