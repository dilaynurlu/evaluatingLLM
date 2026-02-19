import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_types():
    """
    Test _basic_auth_str with mixed string and bytes inputs.
    This ensures that the string input is encoded to latin1 while the bytes input is left as-is,
    and they are successfully joined.
    """
    username = "user"
    password = b"password"
    
    # Logic: username (str) -> latin1 bytes. password (bytes) -> unchanged.
    username_bytes = username.encode("latin1")
    raw_bytes = b":".join((username_bytes, password))
    
    expected_b64 = base64.b64encode(raw_bytes).decode("ascii")
    expected_auth_str = "Basic " + expected_b64
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0
        
    assert result == expected_auth_str