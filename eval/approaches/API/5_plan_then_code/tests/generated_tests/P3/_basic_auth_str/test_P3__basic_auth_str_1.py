import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_standard_strings_and_integrity():
    """
    Test _basic_auth_str with standard ASCII string inputs.
    Refined to verify the result by decoding the output (round-trip verification)
    rather than reconstructing the implementation logic.
    Also verifies edge cases: long strings (no line wrapping) and colons in credentials.
    """
    username = "Aladdin"
    password = "open_sesame"
    
    result = _basic_auth_str(username, password)
    
    # Verify structure
    assert result.startswith("Basic ")
    token = result.split(" ")[1]
    
    # Verify content by decoding
    decoded_bytes = base64.b64decode(token)
    decoded_str = decoded_bytes.decode("latin1")
    assert decoded_str == f"{username}:{password}"

    # Edge Case: Long payload
    # Ensure no newlines are inserted (some Base64 implementations wrap at 76 chars)
    long_user = "u" * 100
    long_pass = "p" * 100
    long_result = _basic_auth_str(long_user, long_pass)
    assert "\n" not in long_result
    
    # Edge Case: Colon in username
    # Verifies that a colon is included literally, even if it creates ambiguity
    col_user = "user:name"
    col_pass = "password"
    col_result = _basic_auth_str(col_user, col_pass)
    col_token = col_result.split(" ")[1]
    col_decoded = base64.b64decode(col_token).decode("latin1")
    assert col_decoded == f"{col_user}:{col_pass}"