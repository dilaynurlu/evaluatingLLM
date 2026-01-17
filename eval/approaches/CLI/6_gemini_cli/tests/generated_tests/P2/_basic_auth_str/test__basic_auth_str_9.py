import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    # Scenario: Bytes username, String password
    # b'user', 'pass'
    result = _basic_auth_str(b"user", "pass")
    assert result == "Basic dXNlcjpwYXNz"
