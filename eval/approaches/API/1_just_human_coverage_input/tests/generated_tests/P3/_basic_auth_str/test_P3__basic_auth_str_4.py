from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_str_and_bytes():
    username = "user_str"
    password = b"pass_bytes"
    
    # Golden Master Calculation:
    # "user_str" (latin1 encoded) + b":" + b"pass_bytes"
    # Combined: b"user_str:pass_bytes"
    # Base64: dXNlcl9zdHI6cGFzc19ieXRlcw==
    expected = "Basic dXNlcl9zdHI6cGFzc19ieXRlcw=="
    
    result = _basic_auth_str(username, password)
    assert result == expected