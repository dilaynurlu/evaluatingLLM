import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_str_and_bytes():
    """
    Test _basic_auth_str with mixed string and bytes inputs.
    Verifies that the function handles a combination of string and bytes correctly
    by encoding the string component to bytes (latin1) and joining with the bytes component.
    """
    username = "user_str"
    password = b"pass_bytes"

    # Implementation logic:
    # String username -> encoded to latin1 bytes
    # Bytes password -> remains bytes
    user_bytes = username.encode("latin1")
    pass_bytes = password
    raw = b":".join((user_bytes, pass_bytes))
    expected_b64 = base64.b64encode(raw).decode("ascii")
    expected_auth_str = "Basic " + expected_b64

    result = _basic_auth_str(username, password)

    assert result == expected_auth_str