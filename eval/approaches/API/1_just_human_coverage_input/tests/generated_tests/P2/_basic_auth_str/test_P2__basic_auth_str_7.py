import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecated_none_input():
    """
    Test _basic_auth_str with None as input.
    Verifies that passing None triggers a DeprecationWarning and is converted 
    to the string "None".
    """
    username = "user"
    password = None

    # Expected behavior:
    # password becomes "None" (str)
    user_bytes = username.encode("latin1")
    pass_bytes = str(password).encode("latin1")
    raw = b":".join((user_bytes, pass_bytes))
    expected_b64 = base64.b64encode(raw).decode("ascii")
    expected_auth_str = "Basic " + expected_b64

    with pytest.warns(DeprecationWarning, match="Non-string .* will no longer be supported"):
        result = _basic_auth_str(username, password)

    assert result == expected_auth_str