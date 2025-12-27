import base64
from requests.auth import _basic_auth_str

def test_basic_auth_str_standard_ascii():
    """
    Test _basic_auth_str with standard ASCII string inputs.
    Verifies that strings are encoded and formatted correctly into a Basic Auth header.
    """
    username = "testuser"
    password = "testpassword"
    
    # Expected logic:
    # 1. Strings are encoded to latin1 (ASCII is a subset).
    # 2. Joined with ':' -> b"testuser:testpassword"
    # 3. Base64 encoded.
    # 4. Prefixed with "Basic ".
    
    combined = f"{username}:{password}".encode("latin1")
    encoded_part = base64.b64encode(combined).decode("utf-8")
    expected_auth_str = f"Basic {encoded_part}"
    
    assert _basic_auth_str(username, password) == expected_auth_str