import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_bytes_input():
    """Test _basic_auth_str with bytes inputs."""
    username = b"Aladdin"
    password = b"open sesame"
    expected = "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    
    result = _basic_auth_str(username, password)
    assert result == expected
