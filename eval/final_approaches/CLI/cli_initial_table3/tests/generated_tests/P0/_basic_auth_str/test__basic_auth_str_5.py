from requests.auth import _basic_auth_str

def test_basic_auth_str_5():
    # '£' is \xa3 in latin1. 
    # 'user£' encoded as latin1 is b'user\xa3'
    # b64encode(b'user\xa3:password') -> b'dXNlcpM6cGFzc3dvcmQ='
    username = "user£"
    password = "password"
    expected = "Basic dXNlcqM6cGFzc3dvcmQ="
    assert _basic_auth_str(username, password) == expected
