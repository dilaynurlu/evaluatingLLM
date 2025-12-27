import pytest
from unittest.mock import MagicMock
from requests.auth import HTTPDigestAuth
import requests

def test_digest_auth_handle_redirect():
    """
    Test that handle_redirect resets the num_401_calls counter.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Initialize
    req = MagicMock(spec=requests.PreparedRequest)
    req.register_hook = MagicMock()
    req.body = None
    auth(req)
    
    # Set counter to something else
    auth._thread_local.num_401_calls = 10
    
    r = MagicMock(spec=requests.Response)
    r.is_redirect = True
    
    auth.handle_redirect(r)
    
    assert auth._thread_local.num_401_calls == 1