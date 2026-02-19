import pytest
from requests.utils import unquote_header_value

def test_unquote_removes_surrounding_quotes():
    """
    Test that surrounding double quotes are stripped from the string.
    """
    input_value = '"quoted text"'
    result = unquote_header_value(input_value)
    assert result == "quoted text"