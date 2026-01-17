
import pytest
from requests.auth import _basic_auth_str

def test__basic_auth_str_deprecation_int_username():
    with pytest.warns(DeprecationWarning, match="Non-string usernames will no longer be supported"):
        auth_str = _basic_auth_str(123, "password")
    assert "Basic " in auth_str
