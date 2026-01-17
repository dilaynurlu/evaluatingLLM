import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_latin1_characters():
    """
    Test _basic_auth_str with strings containing Latin-1 characters (extended ASCII).
    Verifies that characters like 'ñ' or '£' are encoded using latin1 as expected
    by the implementation, not utf-8.
    """
    # 'ñ' is \xf1 in latin1. '£' is \xa3 in latin1.
    username = "ElNiño"
    password = "£50"

    # Construction with explicit latin1 encoding
    user_bytes = username.encode("latin1")
    pass_bytes = password.encode("latin1")
    raw = b":".join((user_bytes, pass_bytes))
    expected_b64 = base64.b64encode(raw).decode("ascii")
    expected_auth_str = "Basic " + expected_b64

    result = _basic_auth_str(username, password)

    assert result == expected_auth_str