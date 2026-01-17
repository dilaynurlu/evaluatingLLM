
import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_ne_username():
    auth1 = HTTPDigestAuth("user1", "pass")
    auth2 = HTTPDigestAuth("user2", "pass")
    assert auth1 != auth2
