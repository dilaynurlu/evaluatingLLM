import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_strings():
    """
    Test _basic_auth_str with strings containing non-ASCII but valid Latin1 characters.
    """
    username = "userñ"
    password = "passü"
    
    result = _basic_auth_str(username, password)
    
    raw_payload = (username + ":" + password).encode("latin1")
    expected_b64 = base64.b64encode(raw_payload).decode("ascii")
    expected = "Basic " + expected_b64
    
    assert result == expected