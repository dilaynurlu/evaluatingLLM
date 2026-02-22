import pytest
import warnings
from requests.auth import _basic_auth_str

def test__basic_auth_str_deprecation_warning_on_int():
    """
    Test that DeprecationWarning is issued when passing non-string/bytes (e.g. int).
    """
    with pytest.warns(DeprecationWarning):
        _basic_auth_str(123, 456)
