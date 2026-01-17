from requests.auth import _basic_auth_str
import base64

def test_basic_auth_str_bytes_input():
    # If bytes are passed, they are not encoded again if not instance of str
    # Wait, code says:
    # if isinstance(username, str): username = username.encode('latin1')
    # So if I pass bytes, it skips encoding and joins them directly?
    # "b':'.join((username, password))" -> expects bytes if one is bytes
    
    username = b"user"
    password = b"password"
    expected = "Basic " + base64.b64encode(b"user:password").decode("utf-8")
    assert _basic_auth_str(username, password) == expected
