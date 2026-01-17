import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_inputs():
    """
    Test _basic_auth_str with empty strings.
    Should produce 'Basic ' + base64(':').
    """
    username = ""
    password = ""
    
    # b64encode(b":") -> b"Og=="
    expected_token = base64.b64encode(b":").decode("utf-8")
    expected_auth_str = "Basic " + expected_token
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0

    assert result == expected_auth_str