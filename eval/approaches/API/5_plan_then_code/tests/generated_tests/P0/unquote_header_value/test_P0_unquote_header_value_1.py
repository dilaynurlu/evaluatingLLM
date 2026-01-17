import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_basic_string():
    """
    Test unquoting a basic string that has no quotes.
    Should return the value as-is.
    """
    input_val = "simple_value"
    expected = "simple_value"
    assert unquote_header_value(input_val) == expected