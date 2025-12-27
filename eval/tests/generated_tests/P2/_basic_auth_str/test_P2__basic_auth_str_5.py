import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_deprecation_warning_password():
    """
    Test that passing a non-basestring (e.g., int) password triggers a DeprecationWarning
    and correctly converts the input to a string before encoding.
    """
    username = "admin"
    password = 9876
    
    # "admin:9876" -> b64 -> "Basic YWRtaW46OTg3Ng=="
    expected_auth_str = "Basic YWRtaW46OTg3Ng=="
    
    with pytest.warns(DeprecationWarning, match="Non-string passwords will no longer be supported"):
        result = _basic_auth_str(username, password)
        
    assert result == expected_auth_str