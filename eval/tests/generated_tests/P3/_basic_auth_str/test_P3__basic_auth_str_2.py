import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_credentials():
    """
    Test _basic_auth_str with Latin-1 characters.
    Verifies that characters are correctly encoded to Latin-1 before Base64.
    """
    # 'ñ' is \xf1, '£' is \xa3 in Latin-1
    test_user = "user\u00f1"
    test_pass = "pass\u00a3"
    
    result = _basic_auth_str(test_user, test_pass)
    
    assert result.startswith("Basic ")
    token = result.split(" ", 1)[1]
    
    # Verify by decoding the result back to the original inputs
    # If the function used a different encoding (like utf-8), this decode would fail or mismatch
    decoded_bytes = base64.b64decode(token)
    decoded_str = decoded_bytes.decode("latin1")
    
    assert decoded_str == f"{test_user}:{test_pass}"