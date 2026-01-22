import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_unicode_error():
    """
    Test that passing characters outside the Latin1 range raises a UnicodeEncodeError.
    This verifies that the function enforces Latin1 encoding for string inputs.
    """
    username = "user☃"  # Snowman character is not valid in Latin1
    password = "pass"
    
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str(username, password)