import pytest
import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_string_and_empty_inputs():
    """
    Test _basic_auth_str with non-string inputs (triggering DeprecationWarning)
    and empty string inputs.
    Covers type conversion and warning generation branches.
    """
    # Test case 1: Non-string inputs
    non_string_username = 12345
    non_string_password = None

    # Expected behavior:
    # 1. DeprecationWarning issued for both username and password.
    # 2. Inputs converted to str: "12345", "None"
    # 3. Encoded to latin1 bytes: b"12345", b"None"
    # 4. Joined: b"12345:None"
    # 5. Base64 encoded: b'MTIzNDU6Tm9uZQ=='
    expected_auth_bytes_non_string = b":".join(
        (str(non_string_username).encode("latin1"), str(non_string_password).encode("latin1"))
    )
    encoded_credentials_non_string = base64.b64encode(expected_auth_bytes_non_string).decode("ascii")
    expected_output_non_string = f"Basic {encoded_credentials_non_string}"

    with pytest.warns(DeprecationWarning) as record:
        result = _basic_auth_str(non_string_username, non_string_password)

    assert result == expected_output_non_string
    assert len(record) == 2  # Expecting two DeprecationWarnings
    assert "Non-string usernames will no longer be supported" in str(record[0].message)
    assert "Non-string passwords will no longer be supported" in str(record[1].message)

    # Test case 2: Empty string inputs
    empty_username = ""
    empty_password = ""

    # Expected behavior:
    # 1. Encoded to latin1 bytes: b"", b""
    # 2. Joined: b":"
    # 3. Base64 encoded: b'Og=='
    expected_auth_bytes_empty = b":".join((empty_username.encode("latin1"), empty_password.encode("latin1")))
    encoded_credentials_empty = base64.b64encode(expected_auth_bytes_empty).decode("ascii")
    expected_output_empty = f"Basic {encoded_credentials_empty}"

    result_empty = _basic_auth_str(empty_username, empty_password)
    assert result_empty == expected_output_empty