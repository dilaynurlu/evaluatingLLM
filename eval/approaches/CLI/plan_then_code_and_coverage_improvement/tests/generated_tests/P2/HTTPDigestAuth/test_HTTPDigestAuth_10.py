import threading
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_thread_safety():
    auth = HTTPDigestAuth("user", "pass")
    
    def worker():
        auth.init_per_thread_state()
        auth._thread_local.last_nonce = threading.current_thread().name
    
    t1 = threading.Thread(target=worker, name="t1")
    t2 = threading.Thread(target=worker, name="t2")
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    # Main thread state shouldn't be affected (it's empty yet)
    auth.init_per_thread_state()
    assert auth._thread_local.last_nonce == ""
