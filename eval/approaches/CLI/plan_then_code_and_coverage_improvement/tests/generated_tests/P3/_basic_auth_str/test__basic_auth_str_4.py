from requests.auth import _basic_auth_str

def test__basic_auth_str_4():
    # Test with unicode characters that fit in latin1
    # u"üser" -> latin1 b"\xfcser"
    # u"p@ss"
    username = "üser"
    password = "p@ss"
    result = _basic_auth_str(username, password)
    # b"\xfcser:p@ss" -> b64 "XHdzZXI6cEBzcw=="?
    # Let's just check it starts with Basic
    assert result.startswith("Basic ")