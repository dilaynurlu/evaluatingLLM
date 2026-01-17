import base64
import warnings
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_integers_deprecated():
    """
    Test _basic_auth_str with integer inputs.
    Verifies that passing non-string/non-bytes objects triggers a DeprecationWarning
    and that the values are converted to strings before encoding.
    """
    username = 12345
    password = 67890

    # Expected calculation:
    # Inputs converted to str
    user_str = str(username)
    pass_str = str(password)
    # Then encoded to latin1
    raw_creds = user_str.encode("latin1") + b":" + pass_str.encode("latin1")
    expected_b64 = base64.b64encode(raw_creds).decode("ascii")
    expected_auth = "Basic " + expected_b64

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Verify the output is correct despite deprecation
        assert result == expected_auth

        # Verify warnings were issued
        # We expect DeprecationWarning for both username and password
        assert len(w) >= 2
        dep_warnings = [x for x in w if issubclass(x.category, DeprecationWarning)]
        assert len(dep_warnings) >= 2
        
        # Check message content roughly matches expectation
        assert "Non-string usernames" in str(dep_warnings[0].message) or "Non-string passwords" in str(dep_warnings[0].message)