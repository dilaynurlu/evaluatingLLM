import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_4():
    # Bytes inputs
    result = _basic_auth_str(b"user", b"pass")
    assert result == "Basic dXNlcjpwYXNz"
