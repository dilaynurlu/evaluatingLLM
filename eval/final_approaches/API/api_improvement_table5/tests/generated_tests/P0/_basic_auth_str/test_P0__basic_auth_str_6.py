import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_password():
    """
    Test non-string/non-bytes password input (e.g. float).
    Should trigger a DeprecationWarning and convert the input to string.
    """
    username = "username"
    password = 3.14159
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Verify warning
        assert len(w) > 0
        assert issubclass(w[0].category, DeprecationWarning)
        assert "Non-string passwords" in str(w[0].message)
        
    # Verify the result uses the string representation of the float
    password_str = str(password)
    joined = (username + ":" + password_str).encode("latin1")
    b64_val = base64.b64encode(joined).decode("ascii")
    expected = f"Basic {b64_val}"
    
    assert result == expected