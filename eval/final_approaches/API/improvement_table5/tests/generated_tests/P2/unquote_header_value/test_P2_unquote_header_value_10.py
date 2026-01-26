import pytest
from requests.utils import unquote_header_value

def test_unquote_single_quotes_ignored():
    """
    Test that single quotes are not treated as quote characters by this function
    (it only looks for double quotes).
    """
    input_value = "'single quotes'"
    result = unquote_header_value(input_value)
    assert result == "'single quotes'"