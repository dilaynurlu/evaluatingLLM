from requests.auth import _basic_auth_str

def test_basic_auth_str_bytes():
    # Bytes should be handled without warning if possible, or converted
    res = _basic_auth_str(b"user", b"pass")
    assert res == "Basic dXNlcjpwYXNz"
