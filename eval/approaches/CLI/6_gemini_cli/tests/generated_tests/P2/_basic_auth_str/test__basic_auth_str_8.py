import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_long_string():
    # Scenario: Long strings
    username = "a" * 100
    password = "b" * 100
    result = _basic_auth_str(username, password)
    assert result.startswith("Basic ")
    assert "\n" not in result # valid header should not have newlines
