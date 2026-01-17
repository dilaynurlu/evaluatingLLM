import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecated_int_inputs():
    """
    Test _basic_auth_str with integer inputs.
    Verifies that passing non-string/non-bytes objects (like ints) raises a 
    DeprecationWarning and converts the inputs to strings before processing.
    """
    username = 12345
    password = 67890

    # Expected behavior:
    # 1. Inputs converted to str: "12345", "67890"
    # 2. Then standard processing
    user_str = str(username)
    pass_str = str(password)
    
    user_bytes = user_str.encode("latin1")
    pass_bytes = pass_str.encode("latin1")
    raw = b":".join((user_bytes, pass_bytes))
    expected_b64 = base64.b64encode(raw).decode("ascii")
    expected_auth_str = "Basic " + expected_b64

    with pytest.warns(DeprecationWarning, match="Non-string .* will no longer be supported"):
        result = _basic_auth_str(username, password)

    assert result == expected_auth_str