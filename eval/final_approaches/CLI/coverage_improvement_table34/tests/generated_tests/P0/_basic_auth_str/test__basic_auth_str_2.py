from requests.auth import _basic_auth_str

def test_basic_auth_str_2():
    # Test with bytes
    username = b"user"
    password = b"password"
    expected = "Basic dXNlcjpwYXNzd29yZA=="
    assert _basic_auth_str(username, password) == expected
