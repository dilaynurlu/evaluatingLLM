import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1():
    username = "user\u00A9" # Copyright symbol
    password = "pass\u00A9"
    # \u00A9 encoded in latin1 is \xA9
    expected_bytes = b"user\xA9:pass\xA9"
    expected = "Basic " + base64.b64encode(expected_bytes).decode("ascii")
    assert _basic_auth_str(username, password) == expected
