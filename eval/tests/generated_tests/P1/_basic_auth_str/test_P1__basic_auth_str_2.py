import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_chars():
    """
    Test _basic_auth_str with strings containing Latin1 characters.
    Verifies that the function correctly encodes inputs using latin1 before Base64 encoding.
    """
    # 'ñ' is \xf1 (241) in latin1
    # 'ü' is \xfc (252) in latin1
    username = "niño"
    password = "münchen"
    
    # Manual expectation construction:
    # Enforce latin1 encoding to match function behavior
    u_bytes = username.encode("latin1")
    p_bytes = password.encode("latin1")
    
    combined = u_bytes + b":" + p_bytes
    encoded_part = base64.b64encode(combined).decode("utf-8")
    expected_auth_str = f"Basic {encoded_part}"
    
    assert _basic_auth_str(username, password) == expected_auth_str