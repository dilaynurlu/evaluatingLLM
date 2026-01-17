from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_credentials():
    # 'ñ' is valid in latin1 (0xF1).
    # Using specific test values to verify encoding handling.
    username = "niño"
    password = "contraseña"
    
    # Golden Master Calculation:
    # String: "niño:contraseña"
    # Hex (Latin-1): 6e 69 f1 6f 3a 63 6f 6e 74 72 61 73 65 f1 61
    # Base64: bmlxfW86Y29udHJhc2VxfWE=
    expected = "Basic bmlxfW86Y29udHJhc2VxfWE="
    
    result = _basic_auth_str(username, password)
    assert result == expected