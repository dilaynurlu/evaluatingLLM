import pytest
from requests.utils import unquote_header_value

def test_unquote_header_value_no_quotes():
    """
    Test that strings without any quotes are returned as-is.
    """
    header_value = 'plain_value'
    result = unquote_header_value(header_value)
    assert result == 'plain_value'