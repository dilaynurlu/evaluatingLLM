import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_3():
    # Test with integers (deprecated behavior)
    username = 123
    password = 456
    
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(username, password)
    
    # "123:456" -> base64
    expected = "Basic MTIzOjQ1Ng=="
    assert result == expected
