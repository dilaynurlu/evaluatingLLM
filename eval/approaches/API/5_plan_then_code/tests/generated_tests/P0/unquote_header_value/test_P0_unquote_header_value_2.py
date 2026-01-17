import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_quoted_string():
    """
    Test unquoting a simple double-quoted string.
    Should strip the quotes.
    """
    input_val = '"quoted_value"'
    expected = "quoted_value"
    assert unquote_header_value(input_val) == expected