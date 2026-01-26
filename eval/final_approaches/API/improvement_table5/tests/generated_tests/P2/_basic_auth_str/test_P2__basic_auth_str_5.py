import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_binary_bytes():
    """
    Test _basic_auth_str with bytes containing non-ASCII values (binary data).
    This confirms that bytes are treated as opaque data and not subjected to text encoding rules.
    """
    # 0xFF and 0x00 are not printable ASCII, ensuring we test binary safety.
    username = b"\xff\xfe"
    password = b"\x00\x01"
    
    raw_bytes = b":".join((username, password))
    expected_b64 = base64.b64encode(raw_bytes).decode("ascii")
    expected_auth_str = "Basic " + expected_b64
    
    result = _basic_auth_str(username, password)
    assert result == expected_auth_str