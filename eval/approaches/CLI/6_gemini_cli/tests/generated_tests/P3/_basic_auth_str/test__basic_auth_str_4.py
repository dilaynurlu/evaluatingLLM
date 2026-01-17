from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_both_empty():
    username = ""
    password = ""
    expected = "Basic " + base64.b64encode(b":").decode("utf-8")
    assert _basic_auth_str(username, password) == expected
