import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_empty():
    username = ""
    password = ""
    expected = "Basic " + base64.b64encode(b":").decode("ascii")
    assert _basic_auth_str(username, password) == expected
