import pytest
from requests.utils import unquote_header_value

def test_unquote_empty_cases():
    """
    Test edge cases regarding empty content:
    1. A quoted empty string ("") should become an empty string.
    2. A literal empty string ('') should be returned as is (or empty).
    """
    # Case 1: Quoted empty
    header_quoted = '""'
    assert unquote_header_value(header_quoted) == ''

    # Case 2: Literal empty string (not quoted)
    header_empty = ''
    assert unquote_header_value(header_empty) == ''