import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unbalanced_quotes():
    """
    Test that a string with unbalanced quotes (e.g. only at start) is returned as-is.
    """
    value = '"unbalanced'
    expected = '"unbalanced'
    assert unquote_header_value(value) == expected