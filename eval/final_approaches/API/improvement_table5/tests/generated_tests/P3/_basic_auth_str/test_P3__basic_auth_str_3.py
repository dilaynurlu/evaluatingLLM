from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes_input():
    """
    Test _basic_auth_str with bytes input for both username and password.
    
    This validates the branch where inputs are already bytes, skipping the 
    string-to-bytes encoding step.
    
    Input: b"user_bytes" : b"pass_bytes"
    Base64 (user_bytes:pass_bytes): dXNlcl9ieXRlczpwYXNzX2J5dGVz
    """
    username = b"user_bytes"
    password = b"pass_bytes"
    
    expected = "Basic dXNlcl9ieXRlczpwYXNzX2J5dGVz"
    
    result = _basic_auth_str(username, password)
    
    assert result == expected