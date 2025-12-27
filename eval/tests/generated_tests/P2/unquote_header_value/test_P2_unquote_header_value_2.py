import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_unquoted():
    """
    Test that a string without surrounding quotes is returned as-is.
    """
    value = "SimpleString"
    assert unquote_header_value(value) == "SimpleString"