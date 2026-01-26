import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_warn_username():
    """
    Test _basic_auth_str with a non-string/non-bytes username (e.g., int).
    This validates the backwards compatibility layer that emits a DeprecationWarning
    and converts the input to a string.
    """
    username = 12345
    password = "password"
    
    # Logic: Non-string username triggers warning, converts to str(username) -> "12345"
    str_username = str(username)
    raw_bytes = (str_username + ":" + password).encode("latin1")
    expected_b64 = base64.b64encode(raw_bytes).decode("ascii")
    expected_auth_str = "Basic " + expected_b64
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Verify DeprecationWarning
        assert len(w) > 0
        warning = w[0]
        assert issubclass(warning.category, DeprecationWarning)
        assert "Non-string usernames will no longer be supported" in str(warning.message)
        
    assert result == expected_auth_str