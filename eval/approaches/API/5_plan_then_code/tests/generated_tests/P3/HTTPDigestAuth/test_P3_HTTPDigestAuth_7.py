import pytest
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_handle_redirect_reset():
    """
    Test that the retry counter (num_401_calls) is reset upon receiving a redirect.
    This ensures proper handling of auth flows that traverse redirects.
    """
    auth = HTTPDigestAuth("user", "pass")
    req = Request("GET", "http://example.com").prepare()
    auth(req)
    
    # Simulate dirty state from previous attempt
    auth._thread_local.num_401_calls = 2
    
    # 302 Redirect Response
    response = Response()
    response.status_code = 302
    response.headers["Location"] = "/new-location"
    
    auth.handle_redirect(response)
    
    # Assert reset
    assert auth._thread_local.num_401_calls == 1