
import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_eq_none():
    auth = HTTPDigestAuth("user", "pass")
    assert not (auth == None)
