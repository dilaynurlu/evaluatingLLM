import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecated_none():
    """
    Test _basic_auth_str with None inputs.
    This should trigger DeprecationWarning and convert None to 'None'.
    """
    username = None
    password = None
    
    u_bytes = str(None).encode("latin1") # "None"
    p_bytes = str(None).encode("latin1") # "None"
    raw_creds = b":".join((u_bytes, p_bytes))
    expected_token = base64.b64encode(raw_creds).decode("utf-8")
    expected_auth_str = "Basic " + expected_token
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        
        assert len(w) >= 1
        assert any(issubclass(x.category, DeprecationWarning) for x in w)
        
    assert result == expected_auth_str