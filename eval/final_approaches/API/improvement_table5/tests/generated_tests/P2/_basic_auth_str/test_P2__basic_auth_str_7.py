import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_warn_password():
    """
    Test _basic_auth_str with a non-string/non-bytes password (e.g., None).
    This validates the backwards compatibility layer that emits a DeprecationWarning
    and converts the input to a string.
    """
    username = "user"
    password = None
    
    # Logic: Non-string password triggers warning, converts to str(password) -> "None"
    str_password = str(password)
    raw_bytes = (username + ":" + str_password).encode("latin1")
    expected_b64 = base64.b64encode(raw_bytes).decode("ascii")
    expected_auth_str = "Basic " + expected_b64
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        # Verify DeprecationWarning
        assert len(w) > 0
        # Iterate to find the specific password warning if multiple warnings could theoretically be emitted
        # (though here only one is expected)
        found = False
        for warning in w:
            if issubclass(warning.category, DeprecationWarning) and \
               "Non-string passwords will no longer be supported" in str(warning.message):
                found = True
                break
        assert found, "DeprecationWarning for password not found"
        
    assert result == expected_auth_str