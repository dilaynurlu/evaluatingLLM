import pytest
import threading
from unittest.mock import Mock
from requests.auth import HTTPDigestAuth
from requests.models import Request, Response

def test_digest_auth_thread_isolation():
    """
    Test that HTTPDigestAuth maintains separate state for different threads.
    """
    auth = HTTPDigestAuth("user", "pass")
    
    # Thread 1 sends a request and establishes a nonce
    def thread_1_work():
        req = Request("GET", "http://example.com/").prepare()
        auth(req) # Init thread state
        
        r = Response()
        r.status_code = 401
        r.request = req
        r.headers["www-authenticate"] = 'Digest realm="t1", nonce="nonce-t1", qop="auth"'
        r._content = b""
        r.raw = Mock()
        r.connection = Mock()
        r.connection.send.return_value = Response()
        
        auth.handle_401(r)
        
        # Verify state
        assert auth._thread_local.last_nonce == "nonce-t1"
        assert auth._thread_local.chal["realm"] == "t1"

    # Thread 2 sends a different request with different nonce
    def thread_2_work():
        req = Request("GET", "http://example.com/").prepare()
        auth(req) # Init thread state
        
        r = Response()
        r.status_code = 401
        r.request = req
        r.headers["www-authenticate"] = 'Digest realm="t2", nonce="nonce-t2", qop="auth"'
        r._content = b""
        r.raw = Mock()
        r.connection = Mock()
        r.connection.send.return_value = Response()
        
        auth.handle_401(r)
        
        # Verify state
        assert auth._thread_local.last_nonce == "nonce-t2"
        assert auth._thread_local.chal["realm"] == "t2"

    t1 = threading.Thread(target=thread_1_work)
    t2 = threading.Thread(target=thread_2_work)
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    # Ensure checking the main thread doesn't show side effects (it should be empty or distinct)
    # The main thread state should not be initialized unless we called auth() here.
    assert not hasattr(auth._thread_local, "last_nonce") or auth._thread_local.last_nonce == ""