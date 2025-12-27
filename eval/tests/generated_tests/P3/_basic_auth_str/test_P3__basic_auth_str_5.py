import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_password_deprecation_warning():
    """
    Test _basic_auth_str with a non-string (float) password.
    Verifies the DeprecationWarning and the implicit string conversion.
    """
    test_user = "generic_user"
    test_pass_float = 3.14159
    
    with pytest.warns(DeprecationWarning, match="Non-string passwords will no longer be supported"):
        result = _basic_auth_str(test_user, test_pass_float)
    
    assert result.startswith("Basic ")
    token = result.split(" ", 1)[1]
    
    # Verify the float was converted to its string representation
    decoded_str = base64.b64decode(token).decode("latin1")
    assert decoded_str == f"{test_user}:{test_pass_float}"