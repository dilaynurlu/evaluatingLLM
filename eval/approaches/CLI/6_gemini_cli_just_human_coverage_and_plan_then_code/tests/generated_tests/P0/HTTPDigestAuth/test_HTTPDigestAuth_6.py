
import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_thread_state():
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    assert auth._thread_local.init is True
    assert auth._thread_local.last_nonce == ""
    assert auth._thread_local.nonce_count == 0
    assert auth._thread_local.chal == {}
    assert auth._thread_local.pos is None
    assert auth._thread_local.num_401_calls is None
