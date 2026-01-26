import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes():
    username = b"Aladdin"
    password = b"open sesame"
    expected = "Basic " + base64.b64encode(b"Aladdin:open sesame").decode("ascii")
    assert _basic_auth_str(username, password) == expected
