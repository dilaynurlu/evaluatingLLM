import pytest
import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_standard_inputs():
    """
    Test _basic_auth_str with standard string usernames and passwords,
    including very long inputs.
    Covers the typical use case and string encoding to latin1,
    as well as ensuring robustness with maximum length inputs.
    """
    # Test case 1: Standard string inputs
    username = "testuser"
    password = "secure_password123"

    # Expected basic auth string generation:
    # 1. username and password converted to latin1 bytes: b"testuser", b"secure_password123"
    # 2. Joined with colon: b"testuser:secure_password123"
    # 3. Base64 encoded: b'dGVzdHVzZXI6c2VjdXJlX3Bhc3N3b3JkMTIz'
    # 4. Converted to native string (ascii for base64 output): 'dGVzdHVzZXI6c2VjdXJlX3Bhc3N3b3JkMTIz'
    # 5. Prepended with "Basic "
    expected_auth_bytes = b":".join((username.encode("latin1"), password.encode("latin1")))
    encoded_credentials = base64.b64encode(expected_auth_bytes).decode("ascii")
    expected_output = f"Basic {encoded_credentials}"

    result = _basic_auth_str(username, password)
    assert result == expected_output

    # Test case 2: Long username and password inputs
    long_username = "u" * 256  # A reasonably long username
    long_password = "p" * 512  # A reasonably long password

    expected_auth_bytes_long = b":".join((long_username.encode("latin1"), long_password.encode("latin1")))
    encoded_credentials_long = base64.b64encode(expected_auth_bytes_long).decode("ascii")
    expected_output_long = f"Basic {encoded_credentials_long}"

    result_long = _basic_auth_str(long_username, long_password)
    assert result_long == expected_output_long