import pytest
from requests.auth import _basic_auth_str
import warnings

def test__basic_auth_str_3():
    # Int inputs
    with pytest.warns(DeprecationWarning):
        result = _basic_auth_str(123, 456)
    
    # 123:456 -> MTIzOjQ1Ng==
    assert result == "Basic MTIzOjQ1Ng=="
