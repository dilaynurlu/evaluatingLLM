import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_1():
    # Standard username/password
    result = _basic_auth_str("user", "pass")
    assert result == "Basic dXNlcjpwYXNz"
