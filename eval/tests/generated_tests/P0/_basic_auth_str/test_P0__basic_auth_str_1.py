import pytest
import warnings
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_standard_strings():
    """
    Test _basic_auth_str with standard string username and password.
    Ensures correct latin1 encoding and no warnings for valid string inputs.
    This covers the happy path where both inputs are strings and require
    encoding within the function.
    """
    username = "test_user_123"
    password = "secure_password!"
    
    # Calculate expected output
    # Inputs are strings, so they will be encoded to 'latin1' by the function
    # and then joined by b':' before base64 encoding.
    expected_combined_bytes = f"{username}:{password}".encode("latin1")
    expected_b64_bytes = base64.b64encode(expected_combined_bytes).strip()
    # The output of b64encode is bytes which is then converted to a native string
    # (str in Python 3) by requests.utils.to_native_string, using ascii decoding.
    expected_b64_str = expected_b64_bytes.decode("ascii")
    expected_auth_str = f"Basic {expected_b64_str}"

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always") # Ensure all warnings are caught
        result = _basic_auth_str(username, password)

        assert result == expected_auth_str
        # No warnings expected for standard string inputs
        assert len(w) == 0, f"Unexpected warnings: {[str(warn.message) for warn in w]}"