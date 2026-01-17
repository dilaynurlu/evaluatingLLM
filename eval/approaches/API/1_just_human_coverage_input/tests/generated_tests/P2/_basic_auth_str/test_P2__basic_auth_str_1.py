import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_simple_strings():
    """
    Test _basic_auth_str with standard ASCII string inputs.
    Verifies that strings are encoded using latin1 (implicit in implementation) 
    and formatted as a Basic Auth header.
    """
    username = "Aladdin"
    password = "open sesame"

    # Expected construction logic based on implementation details:
    # 1. Strings are encoded to latin1
    # 2. Joined by ':'
    # 3. Base64 encoded
    # 4. Decoded to native string (ascii/utf-8) and prefixed with "Basic "
    user_bytes = username.encode("latin1")
    pass_bytes = password.encode("latin1")
    raw = b":".join((user_bytes, pass_bytes))
    expected_b64 = base64.b64encode(raw).decode("ascii")
    expected_auth_str = "Basic " + expected_b64

    result = _basic_auth_str(username, password)

    assert result == expected_auth_str