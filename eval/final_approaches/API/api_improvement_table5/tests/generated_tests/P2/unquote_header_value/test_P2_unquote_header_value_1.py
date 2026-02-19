import pytest
from requests.utils import unquote_header_value

def test_unquote_basic_string():
    """
    Test that a string without surrounding double quotes is returned as-is.
    This validates the False branch of the initial quote check.
    """
    input_value = "simple text"
    result = unquote_header_value(input_value)
    assert result == "simple text"