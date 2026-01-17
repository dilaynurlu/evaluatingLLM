from requests.auth import _basic_auth_str

def test_basic_auth_str_empty_credentials():
    username = ""
    password = ""
    
    # Golden Master Calculation:
    # String: ":"
    # Base64: Og==
    expected = "Basic Og=="
    
    result = _basic_auth_str(username, password)
    assert result == expected