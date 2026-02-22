from requests.auth import _basic_auth_str

def test_basic_auth_str_special_chars():
    username = "u@ser"
    password = "p:assword"
    # base64(u@ser:p:assword) -> dUBzZXI6cDphc3N3b3Jk
    expected = "Basic dUBzZXI6cDphc3N3b3Jk"
    assert _basic_auth_str(username, password) == expected
