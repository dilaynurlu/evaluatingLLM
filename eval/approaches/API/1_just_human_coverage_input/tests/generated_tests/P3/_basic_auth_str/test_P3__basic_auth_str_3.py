from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_credentials():
    username = b"user_bytes"
    password = b"pass_bytes"
    
    # Golden Master Calculation:
    # Bytes joined: b"user_bytes:pass_bytes"
    # Base64: dXNlcl9ieXRlczpwYXNzX2J5dGVz
    expected = "Basic dXNlcl9ieXRlczpwYXNzX2J5dGVz"
    
    result = _basic_auth_str(username, password)
    assert result == expected