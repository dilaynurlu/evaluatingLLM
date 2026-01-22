import base64
import pytest
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_int_inputs_deprecation():
    username = 123
    password = 456
    
    # Logic: ints are converted to str() -> "123", "456"
    u_str = str(username)
    p_str = str(password)
    
    u_bytes = u_str.encode("latin1")
    p_bytes = p_str.encode("latin1")
    raw_token = u_bytes + b":" + p_bytes
    token = base64.b64encode(raw_token).decode("ascii")
    expected = "Basic " + token
    
    # Assert that DeprecationWarning is raised
    with pytest.warns(DeprecationWarning) as records:
        result = _basic_auth_str(username, password)
    
    # Verify functionality matches backwards compatibility promise
    assert result == expected
    
    # Ensure the warning message is relevant
    assert len(records) > 0
    assert any("Non-string" in str(r.message) for r in records)