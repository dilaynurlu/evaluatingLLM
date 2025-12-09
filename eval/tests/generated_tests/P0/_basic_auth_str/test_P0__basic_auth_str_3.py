import pytest
import warnings
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_bytes_inputs():
    """
    Test _basic_auth_str with bytes username and password.
    Ensures no internal encoding to latin1 occurs and no warnings are issued,
    as bytes are considered valid 'basestring' types in the context of requests.
    This covers the branches where inputs are already bytes.
    """
    # Using byte strings that might not be valid 'latin1' if decoded,
    # to confirm they are treated as raw bytes and not re-encoded.
    username_bytes = b"byte_user_\xC3\xA9" # Contains a non-latin1 byte sequence if interpreted as char
    password_bytes = b"byte_pass_\x00\xff" # Contains null and a high-byte

    # Expected behavior:
    # 1. No warnings as bytes are "basestring".
    # 2. No internal `username.encode("latin1")` or `password.encode("latin1")`
    #    because they are already bytes.
    # 3. The byte strings are directly joined by b':' and then base64-encoded.
    
    expected_combined_bytes = b":".join((username_bytes, password_bytes))
    expected_b64_bytes = base64.b64encode(expected_combined_bytes).strip()
    expected_b64_str = expected_b64_bytes.decode("ascii") # b64 output is ASCII safe
    expected_auth_str = f"Basic {expected_b64_str}"

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always") # Ensure all warnings are caught
        result = _basic_auth_str(username_bytes, password_bytes)

        assert result == expected_auth_str
        # No warnings expected for bytes inputs
        assert len(w) == 0, f"Unexpected warnings: {[str(warn.message) for warn in w]}"