from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_normal():
    username = "user"
    password = "password"
    expected = "Basic " + base64.b64encode(b"user:password").decode("utf-8")
    assert _basic_auth_str(username, password) == expected
