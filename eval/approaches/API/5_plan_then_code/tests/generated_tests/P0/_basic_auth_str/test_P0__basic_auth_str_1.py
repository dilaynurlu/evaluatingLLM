import base64
import warnings
from requests.auth import _basic_auth_str

def test_basic_auth_str_simple_ascii():
    """
    Test _basic_auth_str with standard ASCII strings.
    Should produce a valid Basic Auth header string without warnings.
    """
    username = "Aladdin"
    password = "open sesame"
    
    # Prepare expected value locally
    # 1. Encode strings to latin1 bytes
    u_bytes = username.encode("latin1")
    p_bytes = password.encode("latin1")
    # 2. Join with colon byte
    raw_creds = b":".join((u_bytes, p_bytes))
    # 3. Base64 encode and decode to string
    expected_token = base64.b64encode(raw_creds).decode("utf-8")
    expected_auth_str = "Basic " + expected_token
    
    # Capture warnings to ensure no DeprecationWarning is emitted for valid strings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = _basic_auth_str(username, password)
        assert len(w) == 0, f"Expected no warnings for string inputs, got: {[str(x.message) for x in w]}"

    assert result == expected_auth_str