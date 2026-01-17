import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_normal():
    # Scenario: Normal ASCII username and password
    expected = "Basic dXNlcjpwYXNz"  # user:pass -> dXNlcjpwYXNz
    assert _basic_auth_str("user", "pass") == expected
