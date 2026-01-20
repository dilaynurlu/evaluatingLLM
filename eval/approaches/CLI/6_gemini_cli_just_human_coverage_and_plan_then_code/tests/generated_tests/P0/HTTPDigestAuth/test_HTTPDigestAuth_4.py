
import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_ne_password():
    auth1 = HTTPDigestAuth("user", "pass1")
    auth2 = HTTPDigestAuth("user", "pass2")
    assert auth1 != auth2
