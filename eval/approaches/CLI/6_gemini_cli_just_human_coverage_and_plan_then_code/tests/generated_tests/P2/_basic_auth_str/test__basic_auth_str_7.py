import pytest
from requests.auth import _basic_auth_str

def test_basic_auth_str_non_latin1_error():
    # Scenario: Characters outside latin1 range should raise UnicodeEncodeError
    # because code does .encode('latin1')
    with pytest.raises(UnicodeEncodeError):
        _basic_auth_str("user\u1234", "pass")
