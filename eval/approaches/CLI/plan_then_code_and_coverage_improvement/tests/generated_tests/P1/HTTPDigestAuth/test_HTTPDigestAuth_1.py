import pytest
from requests.auth import HTTPDigestAuth

def test_HTTPDigestAuth_init():
    """Test initialization of HTTPDigestAuth."""
    auth = HTTPDigestAuth("user", "pass")
    assert auth.username == "user"
    assert auth.password == "pass"
