import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response
from requests.structures import CaseInsensitiveDict

def test_digest_auth_reset_on_redirect():
    """
    Test that handle_redirect resets the 401 call counter.
    Refined to rely on public methods sequence instead of private attributes.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com/").prepare()
    auth(req)
    
    resp_401 = Response()
    resp_401.status_code = 401
    resp_401.request = req
    resp_401.headers = CaseInsensitiveDict({
        "www-authenticate": 'Digest realm="realm", nonce="nonce", qop="auth"'
    })
    resp_401.raw = Mock()
    resp_401._content = b""
    resp_401.connection = Mock()
    resp_401.connection.send.return_value = Response() # Placeholder
    
    # Step 1: Trigger a 401 retry. Internal counter increments to 1.
    auth.handle_401(resp_401)
    assert resp_401.connection.send.call_count == 1
    
    # Step 2: Trigger another 401 retry (simulating a loop or persistent failure).
    # This hits the limit (max 2 calls normally allowed per flow).
    # Internal counter should increment to 2.
    auth.handle_401(resp_401)
    assert resp_401.connection.send.call_count == 2
    
    # At this point, a third call would fail to retry.
    # auth.handle_401(resp_401) would not increment call_count.
    
    # Step 3: Handle a redirect. This should reset the counter to 0.
    resp_redirect = Response()
    resp_redirect.status_code = 302
    resp_redirect.headers = CaseInsensitiveDict({"Location": "/new"})
    auth.handle_redirect(resp_redirect)
    
    # Step 4: Trigger 401 again. Since counter was reset, this should proceed as a fresh attempt.
    auth.handle_401(resp_401)
    
    # Verify the send count increased (2 -> 3)
    assert resp_401.connection.send.call_count == 3