from requests.auth import _basic_auth_str

def test_basic_auth_str_1():
    # Test with normal strings
    username = "user"
    password = "password"
    expected = "Basic dXNlcjpwYXNzd29yZA=="
    assert _basic_auth_str(username, password) == expected
