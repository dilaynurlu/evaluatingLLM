import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1():
    """
    Test _basic_auth_str with Latin-1 characters (extended ASCII).
    This ensures that the 'latin1' encoding step correctly handles characters
    in the range U+0080 to U+00FF.
    """
    # U+00E9 is 'é', U+00F1 is 'ñ'. Both are valid in ISO-8859-1 (Latin-1).
    username = "user\u00E9"
    password = "pass\u00F1"
    
    raw_bytes = (username + ":" + password).encode("latin1")
    expected_b64 = base64.b64encode(raw_bytes).decode("ascii")
    expected_auth_str = "Basic " + expected_b64
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0
        
    assert result == expected_auth_str