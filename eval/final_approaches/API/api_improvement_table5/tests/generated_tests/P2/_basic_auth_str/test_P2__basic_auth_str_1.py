import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_ascii():
    """
    Test _basic_auth_str with simple ASCII strings.
    This exercises the standard path where inputs are strings and require latin1 encoding.
    """
    username = "user"
    password = "password"
    
    # Calculate expected value
    # Logic: 1. strings are encoded to latin1
    #        2. joined with colon
    #        3. base64 encoded
    #        4. stripped and converted to native string (ascii/utf-8)
    #        5. Prepended with "Basic "
    
    raw_bytes = (username + ":" + password).encode("latin1")
    expected_b64 = base64.b64encode(raw_bytes).decode("ascii")
    expected_auth_str = "Basic " + expected_b64
    
    # Ensure no warnings are emitted for valid string inputs
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, "Unexpected warnings emitted for string inputs"
        
    assert result == expected_auth_str