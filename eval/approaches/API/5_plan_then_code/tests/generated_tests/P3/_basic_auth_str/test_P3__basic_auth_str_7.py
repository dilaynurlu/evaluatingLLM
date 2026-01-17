import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_verification():
    """
    Test _basic_auth_str with characters valid in Latin-1 but outside ASCII.
    Refined to verify correct encoding by decoding the result.
    """
    # 'ñ' is \u00f1, 'ü' is \u00fc
    username = "se\u00f1or"
    password = "m\u00fcller"
    
    result = _basic_auth_str(username, password)
    
    assert result.startswith("Basic ")
    token = result.split(" ")[1]
    decoded_bytes = base64.b64decode(token)
    
    # Verify the decoded bytes match the Latin-1 representation of inputs
    expected_bytes = (username + ":" + password).encode("latin1")
    assert decoded_bytes == expected_bytes