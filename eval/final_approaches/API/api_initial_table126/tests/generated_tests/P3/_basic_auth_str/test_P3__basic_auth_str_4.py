import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    """
    Test _basic_auth_str with mixed string and bytes inputs using static vectors.
    Ensures correct type coercion and concatenation.
    """
    username = "user"
    password = b"secret"
    
    # "user" (str) -> b"user" (latin1)
    # b"secret" (bytes) -> b"secret"
    # Joined: b"user:secret"
    # Base64: dXNlcjpzZWNyZXQ=
    expected_auth_str = "Basic dXNlcjpzZWNyZXQ="

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, "Expected no warnings for mixed valid inputs"

    assert result == expected_auth_str