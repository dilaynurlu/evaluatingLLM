import pytest
import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_special_chars_and_bytes_inputs():
    """
    Test _basic_auth_str with string inputs containing special characters,
    including colons and null bytes, directly provided bytes inputs,
    and Unicode characters unencodable by latin1 (expecting an error).
    Covers handling of diverse string content, direct bytes path,
    and explicitly validates latin1 encoding strictness.
    """
    # Test case 1: String inputs with various special characters
    special_char_username = "user@domain.com"
    special_char_password = "p@ss:word!"

    # Expected basic auth string generation:
    # 1. username and password converted to latin1 bytes (special chars handled): b"user@domain.com", b"p@ss:word!"
    # 2. Joined with colon: b"user@domain.com:p@ss:word!"
    # 3. Base64 encoded: b'dXNlckBkb21haW4uY29tOnBAc3M6d29yZCE='
    expected_auth_bytes_special = b":".join(
        (special_char_username.encode("latin1"), special_char_password.encode("latin1"))
    )
    encoded_credentials_special = base64.b64encode(expected_auth_bytes_special).decode("ascii")
    expected_output_special = f"Basic {encoded_credentials_special}"

    result_special = _basic_auth_str(special_char_username, special_char_password)
    assert result_special == expected_output_special

    # Test case 2: Username containing a colon
    username_with_colon = "user:name"
    password_for_colon = "colon_pass"

    expected_auth_bytes_colon_user = b":".join(
        (username_with_colon.encode("latin1"), password_for_colon.encode("latin1"))
    )
    encoded_credentials_colon_user = base64.b64encode(expected_auth_bytes_colon_user).decode("ascii")
    expected_output_colon_user = f"Basic {encoded_credentials_colon_user}"

    result_colon_user = _basic_auth_str(username_with_colon, password_for_colon)
    assert result_colon_user == expected_output_colon_user

    # Test case 3: Null bytes in inputs
    null_byte_username = "user\x00name"
    null_byte_password = "pass\x00word"

    expected_auth_bytes_null_byte = b":".join(
        (null_byte_username.encode("latin1"), null_byte_password.encode("latin1"))
    )
    encoded_credentials_null_byte = base64.b64encode(expected_auth_bytes_null_byte).decode("ascii")
    expected_output_null_byte = f"Basic {encoded_credentials_null_byte}"

    result_null_byte = _basic_auth_str(null_byte_username, null_byte_password)
    assert result_null_byte == expected_output_null_byte

    # Test case 4: Bytes inputs directly
    bytes_username = b"byte_user"
    bytes_password = b"byte_pass"

    # Expected behavior:
    # 1. Inputs are already bytes, so no encoding/warnings occur.
    # 2. Joined with colon: b"byte_user:byte_pass"
    # 3. Base64 encoded: b'Ynl0ZV91c2VyOmJ5dGVfcGFzcw=='
    expected_auth_bytes_bytes = b":".join((bytes_username, bytes_password))
    encoded_credentials_bytes = base64.b64encode(expected_auth_bytes_bytes).decode("ascii")
    expected_output_bytes = f"Basic {encoded_credentials_bytes}"

    result_bytes = _basic_auth_str(bytes_username, bytes_password)
    assert result_bytes == expected_output_bytes

    # Test case 5: Unicode characters unencodable by latin1 (expect UnicodeEncodeError)
    # Emojis and other scripts are explicitly not representable by latin1.
    unicode_username_non_latin1 = "user😀"
    unicode_password_non_latin1 = "パスワード" # Japanese for 'password'

    with pytest.raises(UnicodeEncodeError) as excinfo_user:
        _basic_auth_str(unicode_username_non_latin1, "valid_password")
    assert "character maps to <undefined>" in str(excinfo_user.value) or "codec can't encode character" in str(excinfo_user.value)

    with pytest.raises(UnicodeEncodeError) as excinfo_pass:
        _basic_auth_str("valid_username", unicode_password_non_latin1)
    assert "character maps to <undefined>" in str(excinfo_pass.value) or "codec can't encode character" in str(excinfo_pass.value)

    with pytest.raises(UnicodeEncodeError) as excinfo_both:
        _basic_auth_str(unicode_username_non_latin1, unicode_password_non_latin1)
    assert "character maps to <undefined>" in str(excinfo_both.value) or "codec can't encode character" in str(excinfo_both.value)