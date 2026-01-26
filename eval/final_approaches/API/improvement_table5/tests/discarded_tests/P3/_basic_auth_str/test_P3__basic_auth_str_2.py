from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_characters():
    """
    Test _basic_auth_str with strings containing Latin-1 characters (non-ASCII).
    
    This ensures that the function correctly encodes non-ASCII but valid Latin-1 
    characters into bytes before Base64 encoding.
    
    Input: "usér:påsswörd"
    Latin-1 Hex: 75 73 e9 72 3a 70 e5 73 73 77 f6 72 64
    Base64: dXPZcjpwZdNzdzxyZA==
    """
    username = "usér"
    password = "påsswörd"
    
    expected = "Basic dXPZcjpwZdNzdzxyZA=="
    
    result = _basic_auth_str(username, password)
    
    assert result == expected