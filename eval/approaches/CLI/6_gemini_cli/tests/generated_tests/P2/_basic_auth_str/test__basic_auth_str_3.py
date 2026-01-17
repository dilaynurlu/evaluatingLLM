import pytest
from requests.auth import _basic_auth_str
import warnings

def test_basic_auth_str_non_string():
    # Scenario: Integer inputs trigger DeprecationWarning and conversion
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(123, 456)
    
    # 123:456 -> MTIzOjQ1Ng==
    expected = "Basic MTIzOjQ1Ng=="
    assert result == expected
