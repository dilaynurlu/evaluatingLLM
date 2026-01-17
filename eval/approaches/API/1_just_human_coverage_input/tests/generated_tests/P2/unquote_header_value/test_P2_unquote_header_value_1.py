import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_simple_quoted_string():
    """
    Test that a simple quoted string is correctly unquoted by stripping the surrounding quotes.
    """
    value = '"simple"'
    expected = "simple"
    assert unquote_header_value(value) == expected