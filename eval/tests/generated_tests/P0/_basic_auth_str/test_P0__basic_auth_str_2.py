import pytest
import warnings
from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_non_string_inputs_and_warnings():
    """
    Test _basic_auth_str with non-string username (int) and password (None).
    Ensures DeprecationWarning is issued for both and inputs are correctly
    converted to strings before encoding. This covers the warning paths
    and the implicit str() conversion behavior.
    """
    username_int = 98765
    password_none = None # NoneType

    # Expected behavior:
    # 1. DeprecationWarning for non-string username.
    # 2. username_int is converted to str("98765").
    # 3. DeprecationWarning for non-string password.
    # 4. password_none is converted to str("None").
    # 5. Both converted strings are then encoded to 'latin1' and base64-encoded.
    
    expected_username_after_conversion = str(username_int)
    expected_password_after_conversion = str(password_none)
    
    expected_combined_bytes = f"{expected_username_after_conversion}:{expected_password_after_conversion}".encode("latin1")
    expected_b64_bytes = base64.b64encode(expected_combined_bytes).strip()
    expected_b64_str = expected_b64_bytes.decode("ascii")
    expected_auth_str = f"Basic {expected_b64_str}"

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always") # Ensure all warnings are caught
        result = _basic_auth_str(username_int, password_none)

        assert result == expected_auth_str
        
        # Expecting two DeprecationWarnings
        assert len(w) == 2, f"Expected 2 warnings, but got {len(w)}: {[str(warn.message) for warn in w]}"
        
        # Check username warning
        username_warning = next((warn for warn in w if "Non-string usernames" in str(warn.message)), None)
        assert username_warning is not None, "DeprecationWarning for username not found."
        assert issubclass(username_warning.category, DeprecationWarning)
        assert f"object you've passed in ({username_int!r})" in str(username_warning.message)

        # Check password warning
        password_warning = next((warn for warn in w if "Non-string passwords" in str(warn.message)), None)
        assert password_warning is not None, "DeprecationWarning for password not found."
        assert issubclass(password_warning.category, DeprecationWarning)
        # Note: the target function's warning message for password uses type(password)!r
        assert f"object you've passed in ({type(password_none)!r})" in str(password_warning.message)