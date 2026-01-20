from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_empty_username():
    username = ""
    password = "password"
    expected = "Basic " + base64.b64encode(b":password").decode("utf-8")
    assert _basic_auth_str(username, password) == expected
