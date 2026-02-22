from requests.auth import _basic_auth_str

def test_basic_auth_str_4():
    username = ""
    password = ""
    expected = "Basic Og=="
    assert _basic_auth_str(username, password) == expected
