import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_non_string_input():
    """Test _basic_auth_str with non-string inputs (should warn and convert)."""
    username = 12345
    password = 67890
    expected = "Basic MTIzNDU6Njc4OTA="
    
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(username, password)
    
    assert result == expected
