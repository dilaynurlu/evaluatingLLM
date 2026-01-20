
import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_deprecation_int_password():
    with pytest.warns(DeprecationWarning, match="Non-string passwords will no longer be supported"):
        auth_str = _basic_auth_str("user", 456)
    assert "Basic " in auth_str
