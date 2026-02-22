from requests.auth import _basic_auth_str
import pytest

def test_basic_auth_str_3():
    username = 123
    password = 456
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(username, password)
    
    expected = "Basic MTIzOjQ1Ng=="
    assert result == expected
