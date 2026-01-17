from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_with_colons():
    username = "user:name"
    password = "pass:word"
    # Basic auth just joins with :, so user:name:pass:word
    expected = "Basic " + base64.b64encode(b"user:name:pass:word").decode("utf-8")
    assert _basic_auth_str(username, password) == expected
