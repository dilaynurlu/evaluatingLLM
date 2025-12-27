import pytest
from requests.utils import unquote_header_value

def test_unquote_none_input():
    """
    Test that None input returns None gracefully.
    This ensures the function handles non-string NoneType without raising TypeError.
    """
    result = unquote_header_value(None)
    assert result is None