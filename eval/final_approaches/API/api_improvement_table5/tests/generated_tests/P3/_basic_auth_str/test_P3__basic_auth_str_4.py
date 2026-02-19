from requests.auth import _basic_auth_str

def test_basic_auth_str_mixed_str_and_bytes():
    """
    Test _basic_auth_str with mixed string and bytes inputs.
    
    This exercises the logic where one argument undergoes encoding (str -> bytes)
    while the other is preserved as is (bytes).
    
    Input: "user_str" (str) : b"pass_bytes" (bytes)
    Combined Bytes: b"user_str:pass_bytes"
    Base64: dXNlcl9zdHI6cGFzc19ieXRlcw==
    """
    username = "user_str"
    password = b"pass_bytes"
    
    expected = "Basic dXNlcl9zdHI6cGFzc19ieXRlcw=="
    
    result = _basic_auth_str(username, password)
    
    assert result == expected