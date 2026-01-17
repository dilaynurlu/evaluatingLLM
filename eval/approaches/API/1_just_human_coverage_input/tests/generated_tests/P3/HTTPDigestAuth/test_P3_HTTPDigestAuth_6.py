import pytest
from unittest.mock import Mock
import requests
from requests.auth import HTTPDigestAuth

def test_http_digest_auth_handle_redirect_reset():
    """
    Test that handle_redirect resets the retry counter.
    We simulate a sequence: 401 -> retry -> 401 (hit limit) -> Redirect -> 401 (should retry).
    """
    auth = HTTPDigestAuth("user", "pass")
    req = requests.Request("GET", "http://example.org").prepare()
    
    # Create responses
    resp_401 = requests.Response()
    resp_401.request = req
    resp_401.status_code = 401
    resp_401.headers["www-authenticate"] = 'Digest realm="r", nonce="n", qop="auth"'
    resp_401._content = b""
    resp_401.raw = Mock()
    
    mock_connection = Mock()
    resp_401.connection = mock_connection
    # The retry returns another 401
    mock_connection.send = Mock(return_value=resp_401)
    
    # 1. Start Auth
    auth(req)
    
    # 2. First 401 -> Trigger retry
    auth.handle_401(resp_401)
    assert mock_connection.send.call_count == 1
    
    # 3. Second 401 (the result of the retry) -> Trigger handle_401 again
    # logic should block retry because we are at limit (count=2 after this?)
    # requests impl: init=0. call 1: num=1. call 2: num=2. if num < 2.
    # so second call should fail to retry.
    auth.handle_401(resp_401)
    assert mock_connection.send.call_count == 1 # No increase
    
    # 4. Now simulate a redirect
    # The auth hook `handle_redirect` should reset the internal counter
    resp_redirect = requests.Response()
    resp_redirect.status_code = 302
    resp_redirect.headers["location"] = "http://example.org/new"
    auth.handle_redirect(resp_redirect)
    
    # 5. Encounter 401 again (on the new redirected location presumably)
    # It should allow a retry now
    auth.handle_401(resp_401)
    assert mock_connection.send.call_count == 2 # Increased by 1