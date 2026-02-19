import pytest
from requests.auth import HTTPDigestAuth
from requests.models import Response

def test_HTTPDigestAuth_handle_redirect():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    auth._thread_local.num_401_calls = 10
    
    r = Response()
    r.status_code = 302
    r.headers = {"Location": "/new"}
    
    # Force is_redirect to be True in case status_code check fails or differs
    # But Response.is_redirect is a property. We can't set it on an instance unless we mock it or subclass.
    # Let's use Mock for Response instead of real Response to be sure.
    from unittest.mock import Mock
    r = Mock(spec=Response)
    r.is_redirect = True
    r.status_code = 302
    
    auth.handle_redirect(r)
    
    assert auth._thread_local.num_401_calls == 1
