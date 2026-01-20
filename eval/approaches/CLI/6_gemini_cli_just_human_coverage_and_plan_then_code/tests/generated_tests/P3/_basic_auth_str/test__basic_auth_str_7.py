from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_latin1_chars():
    username = "user\u00e9"  # é is latin1 encodable
    password = "password"
    expected = "Basic " + base64.b64encode(b"user\xe9:password").decode("utf-8")
    assert _basic_auth_str(username, password) == expected
