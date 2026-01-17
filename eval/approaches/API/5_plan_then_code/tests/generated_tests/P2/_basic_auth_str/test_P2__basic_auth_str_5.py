import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_none_deprecated():
    """
    Test _basic_auth_str with None inputs.
    Verifies that None is converted to string "None", triggers DeprecationWarning,
    and produces a valid Basic Auth header for the string "None".
    """
    username = None
    password = None

    # Expected behavior: None -> "None"
    user_str = "None"
    pass_str = "None"
    
    raw_creds = user_str.encode("latin1") + b":" + pass_str.encode("latin1")
    expected_b64 = base64.b64encode(raw_creds).decode("ascii")
    expected_auth = "Basic " + expected_b64

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        assert result == expected_auth
        assert len(w) >= 2
        assert issubclass(w[0].category, DeprecationWarning)