from requests.auth import _basic_auth_str

def test_basic_auth_str_empty():
    username = ""
    password = ""
    # ":" -> Og==
    expected = "Basic Og=="
    assert _basic_auth_str(username, password) == expected
