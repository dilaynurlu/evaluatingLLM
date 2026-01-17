import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_warning_int_password():
    username = "test_user"
    password = 98765
    
    # Golden Master Calculation:
    # "test_user:98765"
    # Base64: dGVzdF91c2VyOjk4NzY1
    expected = "Basic dGVzdF91c2VyOjk4NzY1"
    
    # Use pytest.warns for cleaner assertion of warnings
    with pytest.warns(DeprecationWarning, match="Non-string passwords"):
        result = _basic_auth_str(username, password)
        
    assert result == expected