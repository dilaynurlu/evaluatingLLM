import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_ascii_credentials():
    """
    Test _basic_auth_str with standard ASCII strings.
    Refined to verify the output by decoding rather than reimplementing logic,
    and includes boundary checks for empty strings and colons.
    """
    # 1. Standard credentials
    test_user = "test_user"
    test_pass = "test_secret"
    
    result = _basic_auth_str(test_user, test_pass)
    
    # Verify structure
    assert result.startswith("Basic ")
    token = result.split(" ", 1)[1]
    
    # Verify content by decoding
    decoded_bytes = base64.b64decode(token)
    decoded_str = decoded_bytes.decode("latin1")
    assert decoded_str == f"{test_user}:{test_pass}"

    # 2. Boundary Analysis: Empty credentials
    # Should result in "Basic " + b64(":")
    result_empty = _basic_auth_str("", "")
    token_empty = result_empty.split(" ", 1)[1]
    assert base64.b64decode(token_empty) == b":"

    # 3. Ambiguity check: Colon in username
    # The function treats it as a literal character, ambiguity is server-side
    colon_user = "user:name"
    result_colon = _basic_auth_str(colon_user, "pass")
    token_colon = result_colon.split(" ", 1)[1]
    assert base64.b64decode(token_colon).decode("latin1") == "user:name:pass"