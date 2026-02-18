import base64
import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_string():
    username = 123
    password = 456
    expected = "Basic " + base64.b64encode(b"123:456").decode("ascii")
    
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(username, password)
    
    assert result == expected
