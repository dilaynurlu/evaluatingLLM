from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes():
    username = b"user"
    password = b"pass"
    # "user:pass" -> dXNlcjpwYXNz
    expected = "Basic dXNlcjpwYXNz"
    assert _basic_auth_str(username, password) == expected
