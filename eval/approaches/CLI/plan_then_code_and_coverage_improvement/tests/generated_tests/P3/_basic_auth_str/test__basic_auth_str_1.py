from requests.auth import _basic_auth_str

def test__basic_auth_str_1():
    # Test with standard string inputs
    result = _basic_auth_str("user", "password")
    # "user:password" -> b64 "dXNlcjpwYXNzd29yZA=="
    assert result == "Basic dXNlcjpwYXNzd29yZA=="