
import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_ne_other_type():
    auth = HTTPDigestAuth("user", "pass")
    assert auth != "some string"
