import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_strings():
    """
    Test _basic_auth_str with standard string inputs.
    Verifies that strings are encoded to latin1, joined, and base64 encoded correctly.
    """
    username = "Aladdin"
    password = "open sesame"

    # Expected calculation based on implementation details:
    # 1. Inputs are str, so encoded to latin1
    user_bytes = username.encode("latin1")
    pass_bytes = password.encode("latin1")
    # 2. Joined with colon
    raw_creds = user_bytes + b":" + pass_bytes
    # 3. Base64 encoded and decoded to ascii (native string)
    expected_b64 = base64.b64encode(raw_creds).decode("ascii")
    expected_auth = "Basic " + expected_b64

    result = _basic_auth_str(username, password)
    
    assert result == expected_auth