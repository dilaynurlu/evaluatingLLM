import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_standard_ascii():
    """
    Test _basic_auth_str with standard ASCII username and password strings.
    Verifies that the strings are latin1 encoded, joined by colon, base64 encoded, 
    and prefixed with 'Basic '.
    """
    username = "Aladdin"
    password = "open sesame"
    
    # Expected behavior construction:
    # 1. Strings are encoded to latin1 (default behavior for str inputs)
    # 2. Joined by ':'
    # 3. Base64 encoded
    # 4. Converted to native string (decoded from bytes)
    # 5. Prepended with "Basic "
    
    u_latin1 = username.encode("latin1")
    p_latin1 = password.encode("latin1")
    
    raw_joined = u_latin1 + b":" + p_latin1
    # base64.b64encode returns bytes in Python 3
    b64_val = base64.b64encode(raw_joined).decode("ascii")
    expected = "Basic " + b64_val
    
    result = _basic_auth_str(username, password)
    
    assert result == expected