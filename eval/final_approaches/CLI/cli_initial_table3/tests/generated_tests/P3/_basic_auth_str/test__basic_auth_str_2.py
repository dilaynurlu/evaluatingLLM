import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_2():
    # Latin1 characters
    # user: 'user£', pass: 'pass€' -> '€' is not latin1, so let's use 'ñ' (latin1)
    # 'ñ' is \xf1 in latin1.
    result = _basic_auth_str("userñ", "pass")
    # userñ:pass -> 75 73 65 72 f1 3a 70 61 73 73
    # b64: dXNlcvE6cGFzcw==
    assert result == "Basic dXNlcvE6cGFzcw=="
