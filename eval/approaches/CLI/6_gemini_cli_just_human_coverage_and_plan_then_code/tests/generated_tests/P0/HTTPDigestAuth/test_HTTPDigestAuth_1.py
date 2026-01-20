
import pytest
from requests.auth import HTTPDigestAuth
import threading

def test_HTTPDigestAuth_init():
    auth = HTTPDigestAuth("user", "pass")
    assert auth.username == "user"
    assert auth.password == "pass"
    assert isinstance(auth._thread_local, threading.local)
