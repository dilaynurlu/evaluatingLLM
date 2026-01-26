import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_normal_strings():
    """Test _basic_auth_str with standard string inputs."""
    username = "Aladdin"
    password = "open sesame"
    expected = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    
    result = _basic_auth_str(username, password)
    assert result == expected
