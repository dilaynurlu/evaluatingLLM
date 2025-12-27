import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_username_deprecation_warning():
    """
    Test _basic_auth_str with a non-string (int) username.
    Verifies the DeprecationWarning and the implicit string conversion.
    """
    test_user_int = 12345
    test_pass = "secure_password"
    
    with pytest.warns(DeprecationWarning, match="Non-string usernames will no longer be supported"):
        result = _basic_auth_str(test_user_int, test_pass)
    
    assert result.startswith("Basic ")
    token = result.split(" ", 1)[1]
    
    # Verify the integer was converted to its string representation
    decoded_str = base64.b64decode(token).decode("latin1")
    assert decoded_str == f"{test_user_int}:{test_pass}"