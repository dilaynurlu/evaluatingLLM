from requests.auth import _basic_auth_str

def test_basic_auth_str_normal():
    username = "user"
    password = "password"
    # base64(user:password) -> dXNlcjpwYXNzd29yZA==
    expected = "Basic dXNlcjpwYXNzd29yZA=="
    assert _basic_auth_str(username, password) == expected
