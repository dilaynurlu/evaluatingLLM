
import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_eq():
    auth1 = HTTPDigestAuth("user", "pass")
    auth2 = HTTPDigestAuth("user", "pass")
    assert auth1 == auth2
