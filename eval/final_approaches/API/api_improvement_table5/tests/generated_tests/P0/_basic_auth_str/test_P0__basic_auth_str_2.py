import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_chars():
    """
    Test strings containing Latin-1 characters (e.g., accented characters).
    Verifies that the function correctly encodes inputs to latin1 before base64.
    """
    username = "usërnâmé"
    password = "pässwörd"
    
    u_bytes = username.encode("latin1")
    p_bytes = password.encode("latin1")
    joined = u_bytes + b":" + p_bytes
    
    b64_val = base64.b64encode(joined).decode("ascii")
    expected = f"Basic {b64_val}"
    
    result = _basic_auth_str(username, password)
    assert result == expected