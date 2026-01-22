import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_with_colons():
    """
    Test values containing colons.
    While a colon in a username might be ambiguous in the 'user:pass' format,
    the implementation should blindly join them.
    """
    username = "user"
    password = "pass:word"
    
    result = _basic_auth_str(username, password)
    
    raw_payload = (username + ":" + password).encode("latin1")
    expected_b64 = base64.b64encode(raw_payload).decode("ascii")
    expected = "Basic " + expected_b64
    
    assert result == expected