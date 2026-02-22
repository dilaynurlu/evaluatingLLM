import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_string():
    username = 123
    password = 456
    # Should warn DeprecationWarning
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(username, password)
    
    # "123:456" -> MTIzOjQ1Ng==
    expected = "Basic MTIzOjQ1Ng=="
    assert result == expected
