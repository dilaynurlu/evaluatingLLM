import pytest
from requests.auth import HTTPDigestAuth
import threading

def test_HTTPDigestAuth_thread_init():
    """Test thread-local state initialization."""
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    
    assert hasattr(auth._thread_local, "init")
    assert auth._thread_local.init is True
    assert auth._thread_local.nonce_count == 0
