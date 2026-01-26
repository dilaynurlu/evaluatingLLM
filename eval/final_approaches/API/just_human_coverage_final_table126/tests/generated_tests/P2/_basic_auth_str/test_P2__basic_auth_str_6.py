import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_none_inputs_deprecation():
    username = None
    password = None
    
    # Logic: None becomes string "None"
    u_str = "None"
    p_str = "None"
    
    u_bytes = u_str.encode("latin1")
    p_bytes = p_str.encode("latin1")
    raw_token = u_bytes + b":" + p_bytes
    token = base64.b64encode(raw_token).decode("ascii")
    expected = "Basic " + token
    
    with pytest.warns(DeprecationWarning, match="Non-string"):
        result = _basic_auth_str(username, password)
        
    assert result == expected