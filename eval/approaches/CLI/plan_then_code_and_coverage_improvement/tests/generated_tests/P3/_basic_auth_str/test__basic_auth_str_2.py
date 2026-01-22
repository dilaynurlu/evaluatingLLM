from requests.auth import _basic_auth_str

def test__basic_auth_str_2():
    # Test with bytes inputs
    result = _basic_auth_str(b"user", b"password")
    assert result == "Basic dXNlcjpwYXNzd29yZA=="