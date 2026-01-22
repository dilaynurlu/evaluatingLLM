from requests.auth import _basic_auth_str
import pytest

def test__basic_auth_str_3():
    # Test with non-string inputs (should warn)
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(123, 456)
    # "123:456" -> b64 "MTIzOjQ1Ng=="
    assert result == "Basic MTIzOjQ1Ng=="
