import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_strings():
    username = 123
    password = 456
    expected = "Basic MTIzOjQ1Ng=="
    
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(username, password)
    
    assert result == expected
