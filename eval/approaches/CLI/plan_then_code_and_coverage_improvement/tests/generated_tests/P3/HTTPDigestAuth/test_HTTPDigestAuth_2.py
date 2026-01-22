from requests.auth import HTTPDigestAuth
import threading

def test_HTTPDigestAuth_2():
    # Thread local state initialization
    auth = HTTPDigestAuth("user", "pass")
    auth.init_per_thread_state()
    assert hasattr(auth._thread_local, "init")
    assert auth._thread_local.nonce_count == 0