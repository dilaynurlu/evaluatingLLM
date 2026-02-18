from requests.auth import _basic_auth_str

def test_basic_auth_str_4():
    # Test with unicode characters
    # 'latin1' encoding is used in the implementation
    username = "u\u00FCser" # uüser
    password = "p\u00E5ssword" # påssword
    
    # "u\xfcser:p\xe5ssword" in latin1 bytes
    # b'u\xfcser:p\xe5ssword'
    
    result = _basic_auth_str(username, password)
    assert result.startswith("Basic ")
