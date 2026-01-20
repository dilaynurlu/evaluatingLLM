from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_empty_password():
    username = "user"
    password = ""
    expected = "Basic " + base64.b64encode(b"user:").decode("utf-8")
    assert _basic_auth_str(username, password) == expected
