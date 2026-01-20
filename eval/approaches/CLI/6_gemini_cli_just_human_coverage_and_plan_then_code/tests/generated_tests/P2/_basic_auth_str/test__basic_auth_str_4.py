import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes():
    # Scenario: Bytes input should be handled (not isinstance(str) -> skipped encoding step)
    # b'user', b'pass'
    result = _basic_auth_str(b"user", b"pass")
    expected = "Basic dXNlcjpwYXNz"
    assert result == expected
