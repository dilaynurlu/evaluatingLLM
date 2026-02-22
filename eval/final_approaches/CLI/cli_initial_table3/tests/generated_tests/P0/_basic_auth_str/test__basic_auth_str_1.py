from requests.auth import _basic_auth_str

def test_basic_auth_str_1():
    username = "Aladdin"
    password = "open sesame"
    expected = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    assert _basic_auth_str(username, password) == expected
